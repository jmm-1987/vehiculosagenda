"""Rutas del módulo Rectificaciones de Peso y Volumen."""
from __future__ import annotations

import re
from datetime import datetime, date
from io import BytesIO

from flask import render_template, request, jsonify, send_file
from flask_login import login_required, current_user
from openpyxl import Workbook

import db
from models import Rectificacion

AGENCIAS = ("Surpaq", "XPO", "TSB", "NTL", "Luis Simoes", "Otros")
ESTADOS = ("Pendiente", "Aceptada", "Rechazada")

# Factores kg/m³. TSB es por tramos: ≤1→200, ≤5→220, >5→250
FACTORES_FIJOS = {
    "NTL": 200.0,
    "Surpaq": 225.0,
    "XPO": 250.0,
    "Luis Simoes": 250.0,
    "Otros": 250.0,
}


def _parse_fecha(val):
    if not val:
        return None
    try:
        return datetime.strptime(val, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        return None


def _parse_float(val):
    if val is None or val == "":
        return None
    try:
        return float(val)
    except (TypeError, ValueError):
        return None


def _pvkg_factor(agencia: str, volumen: float | None = None) -> float | None:
    """Devuelve kg/m³ según agencia. TSB depende del volumen."""
    ag = (agencia or "").strip()
    if ag == "TSB":
        if volumen is None:
            return None
        if volumen <= 1:
            return 200.0
        if volumen <= 5:
            return 220.0
        return 250.0
    return FACTORES_FIJOS.get(ag)


def _pvkg_desde(peso, volumen, agencia: str):
    """
    PVKG = el superior entre peso (kg) y peso volumétrico (m³ × factor).
    Si solo hay uno de los dos, se usa ese.
    """
    candidatos = []
    if peso is not None:
        candidatos.append(float(peso))
    if volumen is not None:
        factor = _pvkg_factor(agencia, volumen)
        if factor is not None:
            candidatos.append(float(volumen) * factor)
        elif not candidatos:
            return None
    if not candidatos:
        return None
    return max(candidatos)


def _as_bool(val) -> bool:
    if isinstance(val, str):
        return val.strip().lower() in ("1", "true", "si", "sí", "yes")
    return bool(val)


def _calcular_campos(data: dict):
    from rectificaciones.tarifas_loader import calcular_importe

    agencia = (data.get("agencia") or "").strip()
    cp_destino = re.sub(r"\D", "", str(data.get("cpDestino", data.get("cp_destino", "")) or ""))[:10]
    pd = _parse_float(data.get("pesoDocumentado", data.get("peso_documentado")))
    pr = _parse_float(data.get("pesoReal", data.get("peso_real")))
    vd = _parse_float(data.get("volDocumentado", data.get("vol_documentado")))
    vr = _parse_float(data.get("volReal", data.get("vol_real")))
    pvkg_doc = _pvkg_desde(pd, vd, agencia)
    pvkg_real = _pvkg_desde(pr, vr, agencia)

    sobredim = _as_bool(data.get("sobredimensionado", False))
    precios_manuales = _as_bool(data.get("preciosManuales", data.get("precios_manuales", False)))

    if precios_manuales:
        importe_doc = _parse_float(data.get("importeDocumentado", data.get("importe_documentado")))
        importe_real = _parse_float(data.get("importeReal", data.get("importe_real")))
    else:
        importe_doc = calcular_importe(agencia, pvkg_doc, cp_destino)
        importe_real = calcular_importe(agencia, pvkg_real, cp_destino)

    if sobredim:
        importe_cobrar = _parse_float(data.get("importeCobrar", data.get("importe_cobrar")))
    elif importe_doc is not None and importe_real is not None:
        # Diferencia doc − real (mismo criterio que peso/volumen)
        importe_cobrar = round(importe_doc - importe_real, 2)
    else:
        importe_cobrar = None

    return {
        "agencia": agencia[:80],
        "expedicion": (data.get("expedicion") or "").strip()[:100],
        "cp_destino": cp_destino,
        "fecha": _parse_fecha(data.get("fecha")),
        "peso_documentado": pd,
        "peso_real": pr,
        "diferencia_peso": (pd - pr) if pd is not None and pr is not None else None,
        "vol_documentado": vd,
        "vol_real": vr,
        "diferencia_vol": (vd - vr) if vd is not None and vr is not None else None,
        "pvkg_documentado": pvkg_doc,
        "pvkg_real": pvkg_real,
        "importe_documentado": importe_doc,
        "importe_real": importe_real,
        "sobredimensionado": sobredim,
        "precios_manuales": precios_manuales,
        "importe_cobrar": importe_cobrar,
    }


def _dict(r: Rectificacion):
    return {
        "id": r.id,
        "fecha": r.fecha.isoformat() if r.fecha else None,
        "expedicion": r.expedicion or "",
        "agencia": r.agencia or "",
        "cpDestino": getattr(r, "cp_destino", None) or "",
        "pesoDocumentado": r.peso_documentado,
        "pesoReal": r.peso_real,
        "diferenciaPeso": r.diferencia_peso,
        "volDocumentado": r.vol_documentado,
        "volReal": r.vol_real,
        "diferenciaVol": r.diferencia_vol,
        "pvkgDocumentado": r.pvkg_documentado,
        "pvkgReal": r.pvkg_real,
        "importeDocumentado": r.importe_documentado,
        "importeReal": r.importe_real,
        "sobredimensionado": bool(r.sobredimensionado),
        "preciosManuales": bool(getattr(r, "precios_manuales", False)),
        "importeCobrar": r.importe_cobrar,
        "estado": r.estado or "Pendiente",
        "usuario": r.usuario or "",
        "createdAt": r.fecha_registro.isoformat() if r.fecha_registro else None,
    }


def _validar_campos(campos: dict):
    if not (campos.get("expedicion") or "").strip():
        return "El nº de expedición es obligatorio."
    if not (campos.get("agencia") or "").strip():
        return "La agencia es obligatoria."
    if campos["agencia"] not in AGENCIAS:
        return "Agencia no válida."
    if campos["agencia"] == "TSB" and not (campos.get("cp_destino") or "").strip():
        return "Para TSB indica el código postal de destino."
    if campos.get("sobredimensionado") and campos.get("importe_cobrar") is None:
        return "Indica el importe a cobrar (sobredimensionado)."
    return None


def register_rectificaciones_routes(app):
    @app.route("/rectificaciones")
    @login_required
    def rectificaciones():
        return render_template("rectificaciones.html")

    @app.route("/api/rectificaciones")
    @login_required
    def api_rectificaciones_list():
        desde = _parse_fecha(request.args.get("desde"))
        hasta = _parse_fecha(request.args.get("hasta"))
        agencia = (request.args.get("agencia") or "").strip()
        estado = (request.args.get("estado") or "").strip()
        expedicion_q = (request.args.get("expedicion") or request.args.get("q") or "").strip()

        q = db.session.query(Rectificacion)
        if desde:
            q = q.filter(Rectificacion.fecha >= desde)
        if hasta:
            q = q.filter(Rectificacion.fecha <= hasta)
        if agencia:
            q = q.filter(Rectificacion.agencia == agencia)
        if estado:
            q = q.filter(Rectificacion.estado == estado)
        if expedicion_q:
            q = q.filter(Rectificacion.expedicion.ilike(f"%{expedicion_q}%"))

        filas = (
            q.order_by(Rectificacion.fecha.desc(), Rectificacion.id.desc())
            .limit(1000)
            .all()
        )
        return jsonify({"ok": True, "items": [_dict(r) for r in filas]})

    @app.route("/api/rectificaciones", methods=["POST"])
    @login_required
    def api_rectificaciones_crear():
        data = request.get_json(silent=True) or {}
        campos = _calcular_campos(data)
        err = _validar_campos(campos)
        if err:
            return jsonify({"ok": False, "error": err}), 400
        estado = (data.get("estado") or "Pendiente").strip()
        if estado not in ESTADOS:
            estado = "Pendiente"
        r = Rectificacion(
            **campos,
            estado=estado,
            usuario=current_user.username if current_user.is_authenticated else "",
            fecha_registro=datetime.now(),
        )
        db.session.add(r)
        db.session.commit()
        return jsonify({"ok": True, "item": _dict(r)})

    @app.route("/api/rectificaciones/<int:item_id>", methods=["PUT", "DELETE"])
    @login_required
    def api_rectificaciones_item(item_id):
        r = db.session.query(Rectificacion).filter_by(id=item_id).first()
        if not r:
            return jsonify({"ok": False, "error": "No encontrada"}), 404

        if request.method == "DELETE":
            db.session.delete(r)
            db.session.commit()
            return jsonify({"ok": True})

        # PUT: actualizar y recalcular
        data = request.get_json(silent=True) or {}
        campos = _calcular_campos(data)
        err = _validar_campos(campos)
        if err:
            return jsonify({"ok": False, "error": err}), 400
        for k, v in campos.items():
            setattr(r, k, v)
        if "estado" in data:
            est = (data.get("estado") or "").strip()
            if est in ESTADOS:
                r.estado = est
        db.session.commit()
        return jsonify({"ok": True, "item": _dict(r)})

    @app.route("/api/rectificaciones/<int:item_id>/estado", methods=["POST"])
    @login_required
    def api_rectificaciones_estado(item_id):
        data = request.get_json(silent=True) or {}
        estado = (data.get("estado") or "").strip()
        if estado not in ESTADOS:
            return jsonify({"ok": False, "error": "Estado no válido"}), 400
        r = db.session.query(Rectificacion).filter_by(id=item_id).first()
        if not r:
            return jsonify({"ok": False, "error": "No encontrada"}), 404
        r.estado = estado
        db.session.commit()
        return jsonify({"ok": True, "item": _dict(r)})

    @app.route("/api/rectificaciones/calcular-importe")
    @login_required
    def api_rectificaciones_calcular_importe():
        from rectificaciones.tarifas_loader import calcular_importe, agencia_con_tarifa, baremo_tsb_por_cp
        agencia = (request.args.get("agencia") or "").strip()
        cp = (request.args.get("cp") or request.args.get("cpDestino") or "").strip()
        kg_doc = _parse_float(request.args.get("pvkgDoc"))
        kg_real = _parse_float(request.args.get("pvkgReal"))
        baremo = baremo_tsb_por_cp(cp) if agencia == "TSB" else None
        return jsonify({
            "ok": True,
            "tieneTarifa": agencia_con_tarifa(agencia),
            "baremo": baremo,
            "importeDocumentado": calcular_importe(agencia, kg_doc, cp),
            "importeReal": calcular_importe(agencia, kg_real, cp),
        })

    @app.route("/api/rectificaciones/exportar")
    @login_required
    def api_rectificaciones_exportar():
        desde = _parse_fecha(request.args.get("desde"))
        hasta = _parse_fecha(request.args.get("hasta"))
        q = db.session.query(Rectificacion)
        if desde:
            q = q.filter(Rectificacion.fecha >= desde)
        if hasta:
            q = q.filter(Rectificacion.fecha <= hasta)
        filas = q.order_by(Rectificacion.fecha.asc(), Rectificacion.id.asc()).all()

        wb = Workbook()
        ws = wb.active
        ws.title = "Rectificaciones"
        headers = [
            "Fecha", "Nº Expedición", "Agencia", "CP Destino",
            "Peso Documentado (kg)", "Peso Real (kg)", "Diferencia Peso (kg)",
            "Vol Documentado (m3)", "Vol Real (m3)", "Diferencia Vol (m3)",
            "PVKG Documentado (kg)", "PVKG Real (kg)",
            "Importe Doc (€)", "Importe Real (€)",
            "Sobredimensionado", "Precios manuales", "Importe a cobrar (€)",
            "Estado", "Usuario",
        ]
        ws.append(headers)
        for r in filas:
            ws.append([
                r.fecha.strftime("%d/%m/%Y") if r.fecha else "",
                r.expedicion or "",
                r.agencia or "",
                getattr(r, "cp_destino", None) or "",
                r.peso_documentado if r.peso_documentado is not None else "",
                r.peso_real if r.peso_real is not None else "",
                r.diferencia_peso if r.diferencia_peso is not None else "",
                r.vol_documentado if r.vol_documentado is not None else "",
                r.vol_real if r.vol_real is not None else "",
                r.diferencia_vol if r.diferencia_vol is not None else "",
                r.pvkg_documentado if r.pvkg_documentado is not None else "",
                r.pvkg_real if r.pvkg_real is not None else "",
                r.importe_documentado if r.importe_documentado is not None else "",
                r.importe_real if r.importe_real is not None else "",
                "Sí" if r.sobredimensionado else "No",
                "Sí" if getattr(r, "precios_manuales", False) else "No",
                r.importe_cobrar if r.importe_cobrar is not None else "",
                r.estado or "Pendiente",
                r.usuario or "",
            ])

        buf = BytesIO()
        wb.save(buf)
        buf.seek(0)
        rango = f"{desde or 'inicio'}_a_{hasta or 'hoy'}"
        return send_file(
            buf,
            as_attachment=True,
            download_name=f"rectificaciones_{rango}.xlsx",
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
