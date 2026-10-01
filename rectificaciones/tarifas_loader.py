"""Carga baremos de tarifas desde Excel (.xls) y calcula importes por kg (PVKG)."""
from __future__ import annotations

import os
import re
from functools import lru_cache

# Agencia UI → fichero de tarifa (solo un baremo EXTREMADURA por ahora)
TARIFA_FILES = {
    "NTL": "tarifa_ntl.xls",
    "Surpaq": "tarifa_surpaq.xls",
}

_TARIFAS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tarifas")


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


def _es_precio_por_kg(umbral_kg: float, precio: float) -> bool:
    """En estos Excel, a partir de ~2000 kg el valor es €/kg (< 1)."""
    return precio < 1.0 or umbral_kg >= 2000


@lru_cache(maxsize=8)
def _cargar_baremos(filename: str) -> tuple[tuple[float, float], ...]:
    """
    Lee la columna K.Vol. (col 0) y EXTREMADURA (col 3).
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
        precio = _parse_num(sheet.cell_value(r, 3) if sheet.ncols > 3 else None)
        if kg is None or precio is None:
            # Fin de bloque numérico
            if rows and not re.match(r"^\d", c0s):
                break
            continue
        rows.append((kg, precio))

    rows.sort(key=lambda x: x[0])
    return tuple(rows)


def baremos_agencia(agencia: str) -> tuple[tuple[float, float], ...] | None:
    filename = TARIFA_FILES.get((agencia or "").strip())
    if not filename:
        return None
    try:
        return _cargar_baremos(filename)
    except Exception as e:
        print(f"Error cargando tarifa {agencia}: {e}")
        return None


def calcular_importe(agencia: str, kg: float | None) -> float | None:
    """
    Calcula el importe (€) según baremo de la agencia y los kg (PVKG).
    - Tramos fijos: se aplica el precio del primer umbral >= kg.
    - Tramos €/kg: importe = kg × precio.
    """
    if kg is None:
        return None
    try:
        kg = float(kg)
    except (TypeError, ValueError):
        return None
    if kg <= 0:
        return None

    baremos = baremos_agencia(agencia)
    if not baremos:
        return None

    elegido = baremos[-1]
    for umbral, precio in baremos:
        if kg <= umbral:
            elegido = (umbral, precio)
            break

    umbral, precio = elegido
    if _es_precio_por_kg(umbral, precio):
        return round(kg * precio, 2)
    return round(precio, 2)


def agencia_con_tarifa(agencia: str) -> bool:
    return (agencia or "").strip() in TARIFA_FILES
