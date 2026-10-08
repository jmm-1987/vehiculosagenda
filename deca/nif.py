"""Normalización de NIF, CIF, DNI y documentos de otros países.

No se comprueba la letra ni el dígito de control. Basta con que el
documento, una vez quitados espacios y signos, tenga entre 4 y 20 caracteres.
"""
import re

_LARGO_MIN = 4
_LARGO_MAX = 20


def normalizar_nif(valor: str) -> str:
    texto = re.sub(r"[^A-Za-z0-9]", "", valor or "").upper()
    if texto.startswith("ES") and len(texto) > 9:
        texto = texto[2:]
    return texto


def nif_valido(valor: str) -> bool:
    texto = normalizar_nif(valor)
    return _LARGO_MIN <= len(texto) <= _LARGO_MAX
