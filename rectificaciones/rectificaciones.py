"""Rutas del módulo Rectificaciones de Peso y Volumen."""
from __future__ import annotations

from datetime import datetime, date
from io import BytesIO

from flask import render_template, request, jsonify, send_file
from flask_login import login_required, current_user
from openpyxl import Workbook

import db
from models import Rectificacion

AGENCIAS = ("Surpaq", "XPO", "TSB", "NTL", "Luis Simoes", "Otros")
ESTADOS = ("Pendiente", "Aceptada", "Rechazada")


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


def _pvkg_factor(agencia: str) -> float:
    return 200.0 if (agencia or "") == "NTL" else 250.0


def _calcular_campos(data: dict):
    agencia = (data.get("agencia") or "").strip()
    pd = _parse_float(data.get("pesoDocumentado", data.get("peso_documentado")))
    pr = _parse_float(data.get("pesoReal", data.get("peso_real")))
    vd = _parse_float(data.get("volDocumentado", data.get("vol_documentado")))
    vr = _parse_float(data.get("volReal", data.get("vol_real")))
    factor = _pvkg_factor(agencia)
    return {
        "agencia": agencia[:80],
        "expedicion": (data.get("expedicion") or "").strip()[:100],
        "fecha": _parse_fecha(data.get("fecha")),
        "peso_documentado": pd,
        "peso_real": pr,
        "diferencia_peso": (pd - pr) if pd is not None and pr is not None else None,
        "vol_documentado": vd,
        "vol_real": vr,
        "diferencia_vol": (vd - vr) if vd is not None and vr is not None else None,
        "pvkg_documentado": (vd * factor) if vd is not None else None,
        "pvkg_real": (vr * factor) if vr is not None else None,
    }


def _dict(r: Rectificacion):
    return {
        "id": r.id,
        "fecha": r.fecha.isoformat() if r.fecha else None,
        "expedicion": r.expedicion or "",
        "agencia": r.agencia or "",
        "pesoDocumentado": r.peso_documentado,
        "pesoReal": r.peso_real,
        "diferenciaPeso": r.diferencia_peso,
        "volDocumentado": r.vol_documentado,
        "volReal": r.vol_real,
        "diferenciaVol": r.diferencia_vol,
        "pvkgDocumentado": r.pvkg_documentado,
        "pvkgReal": r.pvkg_real,
        "estado": r.estado or "Pendiente",
        "usuario": r.usuario or "",
        "createdAt": r.fecha_registro.isoformat() if r.fecha_registro else None,
    }


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

        q = db.session.query(Rectificacion)
        if desde:
            q = q.filter(Rectificacion.fecha >= desde)
        if hasta:
            q = q.filter(Rectificacion.fecha <= hasta)
        if agencia:
            q = q.filter(Rectificacion.agencia == agencia)
        if estado:
            q = q.filter(Rectificacion.estado == estado)

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

    @app.route("/api/rectificaciones/<int:item_id>", methods=["DELETE"])
    @login_required
    def api_rectificaciones_borrar(item_id):
        r = db.session.query(Rectificacion).filter_by(id=item_id).first()
        if not r:
            return jsonify({"ok": False, "error": "No encontrada"}), 404
        db.session.delete(r)
        db.session.commit()
        return jsonify({"ok": True})

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
            "Fecha", "Nº Expedición", "Agencia",
            "Peso Documentado (kg)", "Peso Real (kg)", "Diferencia Peso (kg)",
            "Vol Documentado (m3)", "Vol Real (m3)", "Diferencia Vol (m3)",
            "PVKG Documentado (kg)", "PVKG Real (kg)", "Estado", "Usuario",
        ]
        ws.append(headers)
        for r in filas:
            ws.append([
                r.fecha.strftime("%d/%m/%Y") if r.fecha else "",
                r.expedicion or "",
                r.agencia or "",
                r.peso_documentado if r.peso_documentado is not None else "",
                r.peso_real if r.peso_real is not None else "",
                r.diferencia_peso if r.diferencia_peso is not None else "",
                r.vol_documentado if r.vol_documentado is not None else "",
                r.vol_real if r.vol_real is not None else "",
                r.diferencia_vol if r.diferencia_vol is not None else "",
                r.pvkg_documentado if r.pvkg_documentado is not None else "",
                r.pvkg_real if r.pvkg_real is not None else "",
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
