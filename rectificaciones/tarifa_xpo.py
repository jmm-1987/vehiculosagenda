"""Tarifa XPO: baremos por código postal, mínimo, máximo y un porcentaje de subida."""
from __future__ import annotations

import json
import re

import db
from models import TarifaXpo

BAREMOS = (1, 2, 3)
TRAMOS = (
    ("200", "Hasta 200 kg"),
    ("300", "Hasta 300 kg"),
    ("400", "Hasta 400 kg"),
    ("500", "Hasta 500 kg"),
    ("1000", "Hasta 1.000 kg"),
    ("2000", "Hasta 2.000 kg"),
    ("3000", "Hasta 3.000 kg"),
    ("mas_de_3000", "Más de 3.000 kg"),
)

TARIFA_BASE = {
    "tramos": [
        {"id": "200", "baremo_1": 0.0621, "baremo_2": 0.0745, "baremo_3": 0.0755},
        {"id": "300", "baremo_1": 0.0548, "baremo_2": 0.0657, "baremo_3": 0.0682},
        {"id": "400", "baremo_1": 0.0506, "baremo_2": 0.0607, "baremo_3": 0.0640},
        {"id": "500", "baremo_1": 0.0480, "baremo_2": 0.0576, "baremo_3": 0.0614},
        {"id": "1000", "baremo_1": 0.0403, "baremo_2": 0.0483, "baremo_3": 0.0538},
        {"id": "2000", "baremo_1": 0.0324, "baremo_2": 0.0388, "baremo_3": 0.0452},
        {"id": "3000", "baremo_1": 0.0286, "baremo_2": 0.0343, "baremo_3": 0.0399},
        {"id": "mas_de_3000", "baremo_1": 0.0254, "baremo_2": 0.0305, "baremo_3": 0.0356},
    ],
    "minimos": {"baremo_1": 7.91, "baremo_2": 9.49, "baremo_3": 9.67},
    "maximos": {"baremo_1": 174.61, "baremo_2": 209.53, "baremo_3": 244.45},
}


def cp_xpo(cp) -> str | None:
    s = re.sub(r"\D", "", str(cp or ""))[:5]
    if not s:
        return None
    return s.zfill(5)


def baremo_xpo_por_cp(cp) -> int | None:
    """06800-06899 → 1; el resto de 06… → 2; 10… → 3."""
    s = cp_xpo(cp)
    if not s:
        return None
    n = int(s)
    if 6800 <= n <= 6899:
        return 1
    if s.startswith("06"):
        return 2
    if s.startswith("10"):
        return 3
    return None


def _num(val) -> float | None:
    if val is None or val == "":
        return None
    try:
        n = float(val)
    except (TypeError, ValueError):
        return None
    if n < 0:
        return None
    return n


def _tarifa_valida(datos: dict) -> dict | None:
    if not isinstance(datos, dict):
        return None
    origen = {str(t.get("id")): t for t in datos.get("tramos") or [] if isinstance(t, dict)}
    tramos = []
    for tid, _etiqueta in TRAMOS:
        fila = origen.get(tid)
        if not fila:
            return None
        limpio = {"id": tid}
        for b in BAREMOS:
            n = _num(fila.get(f"baremo_{b}"))
            if n is None:
                return None
            limpio[f"baremo_{b}"] = n
        tramos.append(limpio)
    minimos = {}
    maximos = {}
    for nombre, destino in (("minimos", minimos), ("maximos", maximos)):
        bloque = datos.get(nombre) or {}
        for b in BAREMOS:
            n = _num(bloque.get(f"baremo_{b}"))
            if n is None:
                return None
            destino[f"baremo_{b}"] = n
    return {"tramos": tramos, "minimos": minimos, "maximos": maximos}


def tarifa_publica(porcentaje: float, datos: dict) -> dict:
    etiquetas = dict(TRAMOS)
    tramos = []
    for fila in datos["tramos"]:
        tramos.append({
            "id": fila["id"],
            "etiqueta": etiquetas.get(fila["id"], fila["id"]),
            "unidad": "eur_kg",
            "baremo_1": fila["baremo_1"],
            "baremo_2": fila["baremo_2"],
            "baremo_3": fila["baremo_3"],
        })
    return {
        "porcentaje": porcentaje,
        "moneda": "EUR",
        "tramos": tramos,
        "minimos": datos["minimos"],
        "maximos": datos["maximos"],
    }


def obtener_tarifa() -> tuple[float, dict]:
    fila = db.session.query(TarifaXpo).order_by(TarifaXpo.id).first()
    if fila is None:
        fila = TarifaXpo(porcentaje=0, datos=json.dumps(TARIFA_BASE))
        db.session.add(fila)
        db.session.commit()
    try:
        datos = json.loads(fila.datos or "")
    except json.JSONDecodeError:
        datos = None
    limpio = _tarifa_valida(datos) if isinstance(datos, dict) else None
    if limpio is None:
        limpio = _tarifa_valida(TARIFA_BASE)
        fila.datos = json.dumps(limpio)
        db.session.commit()
    return float(fila.porcentaje or 0), limpio


def guardar_tarifa(porcentaje, datos: dict) -> tuple[float, dict] | str:
    pct = _num(porcentaje)
    if pct is None:
        return "El porcentaje no es válido."
    limpio = _tarifa_valida(datos)
    if limpio is None:
        return "Revisa los precios de la tarifa. Tienen que ser números iguales o mayores que cero."
    fila = db.session.query(TarifaXpo).order_by(TarifaXpo.id).first()
    if fila is None:
        fila = TarifaXpo(porcentaje=pct, datos=json.dumps(limpio))
        db.session.add(fila)
    else:
        fila.porcentaje = pct
        fila.datos = json.dumps(limpio)
    db.session.commit()
    return pct, limpio


def _precio_kg(kg: float, baremo: int, datos: dict) -> float | None:
    clave = f"baremo_{baremo}"
    elegido = None
    for fila in datos["tramos"]:
        if fila["id"] == "mas_de_3000":
            elegido = fila.get(clave)
            continue
        if kg <= float(fila["id"]):
            return float(fila[clave])
    if elegido is None:
        return None
    return float(elegido)


def calcular_importe_xpo(kg: float | None, cp) -> float | None:
    """Precio total: kg × €/kg, sin bajar del mínimo ni pasar del máximo, más el porcentaje."""
    if kg is None:
        return None
    try:
        kg = float(kg)
    except (TypeError, ValueError):
        return None
    if kg <= 0:
        return None
    baremo = baremo_xpo_por_cp(cp)
    if baremo is None:
        return None
    porcentaje, datos = obtener_tarifa()
    eur_kg = _precio_kg(kg, baremo, datos)
    if eur_kg is None:
        return None
    clave = f"baremo_{baremo}"
    total = kg * eur_kg
    minimo = float(datos["minimos"][clave])
    maximo = float(datos["maximos"][clave])
    if total < minimo:
        total = minimo
    elif total > maximo:
        total = maximo
    total = total * (1 + porcentaje / 100.0)
    return round(total, 2)
