"""Validación de NIF, NIE y CIF españoles."""
import re

_LETRAS_NIF = "TRWAGMYFPDXBNJZSQVHLCKE"
_LETRAS_CIF = "ABCDEFGHJNPQRSUVW"
_CIF_SOLO_LETRA = "PQRSNW"
_CIF_SOLO_DIGITO = "ABEH"
_CONTROL_CIF = "JABCDEFGHI"


def normalizar_nif(valor: str) -> str:
    texto = re.sub(r"[^A-Za-z0-9]", "", valor or "").upper()
    if texto.startswith("ES") and len(texto) > 9:
        texto = texto[2:]
    return texto


def nif_valido(valor: str) -> bool:
    texto = normalizar_nif(valor)
    if len(texto) != 9:
        return False
    if texto[0].isdigit():
        return _nif_ok(texto)
    if texto[0] in "XYZ":
        return _nie_ok(texto)
    if texto[0] in _LETRAS_CIF:
        return _cif_ok(texto)
    return False


def _nif_ok(texto: str) -> bool:
    numero, letra = texto[:8], texto[8]
    if not numero.isdigit() or not letra.isalpha():
        return False
    return _LETRAS_NIF[int(numero) % 23] == letra


def _nie_ok(texto: str) -> bool:
    sustituto = {"X": "0", "Y": "1", "Z": "2"}[texto[0]]
    return _nif_ok(sustituto + texto[1:])


def _cif_ok(texto: str) -> bool:
    cuerpo, ultimo = texto[1:8], texto[8]
    if not cuerpo.isdigit():
        return False
    suma_pares = sum(int(cuerpo[i]) for i in range(1, 7, 2))
    suma_impares = 0
    for i in range(0, 7, 2):
        doble = int(cuerpo[i]) * 2
        suma_impares += doble // 10 + doble % 10
    control = (10 - (suma_pares + suma_impares) % 10) % 10
    letra = _CONTROL_CIF[control]
    digito = str(control)
    inicial = texto[0]
    if inicial in _CIF_SOLO_LETRA:
        return ultimo == letra
    if inicial in _CIF_SOLO_DIGITO:
        return ultimo == digito
    return ultimo == digito or ultimo == letra
