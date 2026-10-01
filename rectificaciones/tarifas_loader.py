"""Carga baremos de tarifas desde Excel (.xls) y calcula importes por kg (PVKG)."""
from __future__ import annotations

import os
import re
from functools import lru_cache

# Agencia UI → fichero de tarifa
TARIFA_FILES = {
    "NTL": "tarifa_ntl.xls",
    "Surpaq": "tarifa_surpaq.xls",
    "TSB": "tarifa_tsb.xls",
}

_TARIFAS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tarifas")

# Códigos postales / rangos que usan baremo B en TSB (el resto → C)
_TSB_B_EXACTOS = frozenset({
    6200, 6210, 6220,
    6400,
    6470, 6473,
    6700,
    6800,
    6840,
    10195,
})
_TSB_B_RANGOS = (
    (6000, 6080),
    (10000, 10099),
)


def _parse_num(val) -> float | None:
    if val is None or val == "":
        return None
    if isinstance(val, (int, float)):
        return float(val)
    s = str(val).strip().replace(" ", "")
    if not s:
        return None
    # Formato europeo: 4,54 / 0,0480
    if "," in s and "." in s:
        s = s.replace(".", "").replace(",", ".")
    elif "," in s:
        s = s.replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None


def _es_precio_por_kg(precio: float) -> bool:
    """Valores < 1 en el Excel son €/kg; el resto precio fijo del tramo."""
    return precio < 1.0


def _norm_cp(cp) -> int | None:
    if cp is None:
        return None
    s = re.sub(r"\D", "", str(cp).strip())
    if not s:
        return None
    # Tomar hasta 5 dígitos (CP español)
    s = s[:5]
    try:
        return int(s)
    except ValueError:
        return None


def baremo_tsb_por_cp(cp) -> str:
    """
    Devuelve 'B' o 'C' según CP de destino.
    Todos C excepto los listados (rangos y códigos concretos) → B.
    """
    n = _norm_cp(cp)
    if n is None:
        return "C"
    if n in _TSB_B_EXACTOS:
        return "B"
    for lo, hi in _TSB_B_RANGOS:
        if lo <= n <= hi:
            return "B"
    return "C"


@lru_cache(maxsize=16)
def _cargar_baremos(filename: str, col_precio: int = 3) -> tuple[tuple[float, float], ...]:
    """
    Lee K.Vol. (col 0) y la columna de precio indicada.
    Devuelve tupla ordenada (kg_max, precio).
    """
    import xlrd

    path = os.path.join(_TARIFAS_DIR, filename)
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Tarifa no encontrada: {path}")

    book = xlrd.open_workbook(path)
    sheet = book.sheet_by_index(0)
    rows: list[tuple[float, float]] = []
    en_baremos = False

    for r in range(sheet.nrows):
        c0 = sheet.cell_value(r, 0)
        c0s = str(c0).strip() if c0 is not None else ""
        if c0s.upper() == "BAREMOS":
            en_baremos = True
            continue
        if not en_baremos:
            continue
        if c0s.upper() in ("PLAZAS", "ESPECIALES", "EXENTAS", "ORIGEN", "DESTINO"):
            break
        if c0s.upper() in ("K.VOL.", "K.VOL", "KVOL"):
            continue
        kg = _parse_num(c0)
        precio = _parse_num(sheet.cell_value(r, col_precio) if sheet.ncols > col_precio else None)
        if kg is None or precio is None:
            if rows and not re.match(r"^\d", c0s):
                break
            continue
        rows.append((kg, precio))

    rows.sort(key=lambda x: x[0])
    return tuple(rows)


def baremos_agencia(agencia: str, cp: str | None = None) -> tuple[tuple[float, float], ...] | None:
    ag = (agencia or "").strip()
    filename = TARIFA_FILES.get(ag)
    if not filename:
        return None
    try:
        if ag == "TSB":
            # Col C = 3, Col B = 6
            baremo = baremo_tsb_por_cp(cp)
            col = 6 if baremo == "B" else 3
            return _cargar_baremos(filename, col)
        return _cargar_baremos(filename, 3)
    except Exception as e:
        print(f"Error cargando tarifa {agencia}: {e}")
        return None


def calcular_importe(agencia: str, kg: float | None, cp: str | None = None) -> float | None:
    """
    Calcula el importe (€) según baremo de la agencia y los kg (PVKG).
    Para TSB hace falta el CP de destino (baremo B/C).
    """
    if kg is None:
        return None
    try:
        kg = float(kg)
    except (TypeError, ValueError):
        return None
    if kg <= 0:
        return None

    baremos = baremos_agencia(agencia, cp)
    if not baremos:
        return None

    elegido = baremos[-1]
    for umbral, precio in baremos:
        if kg <= umbral:
            elegido = (umbral, precio)
            break

    _umbral, precio = elegido
    if _es_precio_por_kg(precio):
        return round(kg * precio, 2)
    return round(precio, 2)


def agencia_con_tarifa(agencia: str) -> bool:
    return (agencia or "").strip() in TARIFA_FILES
