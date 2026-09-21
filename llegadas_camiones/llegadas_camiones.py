"""Rutas del Control horario de llegada de camiones."""
from __future__ import annotations

from datetime import datetime, date
from collections import Counter

from flask import render_template, request, jsonify
from flask_login import login_required, current_user

import db
from models import LlegadaCamionDia, LlegadaCamionLinea
from llegadas_camiones.plantilla import RUTAS_PLANTILLA, TURNO_DEFAULT


def _parse_fecha(val):
    if not val:
        return None
    try:
        return datetime.strptime(val, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        return None


def _linea_dict(lin: LlegadaCamionLinea):
    return {
        "id": lin.id,
        "dia_id": lin.dia_id,
        "orden": lin.orden,
        "agencia": lin.agencia or "",
        "ruta": lin.ruta or "",
        "matricula": lin.matricula or "",
        "hora_llegada": lin.hora_llegada or "",
        "fin_descarga": lin.fin_descarga or "",
        "pallets": lin.pallets or "",
        "personas": lin.personas or "",
        "es_manual": bool(lin.es_manual),
    }


def _dia_dict(dia: LlegadaCamionDia, lineas):
    return {
        "id": dia.id,
        "fecha": dia.fecha.isoformat(),
        "turno": dia.turno or TURNO_DEFAULT,
        "lineas": [_linea_dict(l) for l in lineas],
    }


def _obtener_o_crear_dia(fecha: date, turno: str | None = None):
    dia = db.session.query(LlegadaCamionDia).filter_by(fecha=fecha).first()
    if dia:
        lineas = (
            db.session.query(LlegadaCamionLinea)
            .filter_by(dia_id=dia.id)
            .order_by(LlegadaCamionLinea.orden, LlegadaCamionLinea.id)
            .all()
        )
        return dia, lineas

    username = current_user.username if current_user.is_authenticated else ""
    dia = LlegadaCamionDia(
        fecha=fecha,
        turno=(turno or TURNO_DEFAULT)[:100],
        usuario=username,
        fecha_registro=datetime.now(),
    )
    db.session.add(dia)
    db.session.flush()

    lineas = []
    for i, (agencia, ruta) in enumerate(RUTAS_PLANTILLA, start=1):
        lin = LlegadaCamionLinea(
            dia_id=dia.id,
            orden=i,
            agencia=agencia,
            ruta=ruta,
            es_manual=False,
            usuario_mod=username,
            fecha_mod=datetime.now(),
        )
        db.session.add(lin)
        lineas.append(lin)

    db.session.commit()
    return dia, lineas


def register_llegadas_camiones_routes(app):
    @app.route("/llegadas-camiones")
    @login_required
    def llegadas_camiones():
        return render_template("llegadas_camiones.html")

    @app.route("/api/llegadas-camiones/dia")
    @login_required
    def api_llegadas_dia():
        fecha = _parse_fecha(request.args.get("fecha"))
        if not fecha:
            return jsonify({"ok": False, "error": "Fecha no válida"}), 400
        turno = (request.args.get("turno") or "").strip() or None
        dia, lineas = _obtener_o_crear_dia(fecha, turno)
        return jsonify({"ok": True, "dia": _dia_dict(dia, lineas)})

    @app.route("/api/llegadas-camiones/dia/turno", methods=["POST"])
    @login_required
    def api_llegadas_turno():
        data = request.get_json(silent=True) or {}
        fecha = _parse_fecha(data.get("fecha"))
        turno = (data.get("turno") or TURNO_DEFAULT).strip()[:100]
        if not fecha:
            return jsonify({"ok": False, "error": "Fecha no válida"}), 400
        dia, _ = _obtener_o_crear_dia(fecha, turno)
        dia.turno = turno
        db.session.commit()
        return jsonify({"ok": True, "turno": dia.turno})

    @app.route("/api/llegadas-camiones/linea", methods=["POST"])
    @login_required
    def api_llegadas_guardar_linea():
        data = request.get_json(silent=True) or {}
        try:
            linea_id = int(data.get("id"))
        except (TypeError, ValueError):
            return jsonify({"ok": False, "error": "ID no válido"}), 400

        lin = db.session.query(LlegadaCamionLinea).filter_by(id=linea_id).first()
        if not lin:
            return jsonify({"ok": False, "error": "Línea no encontrada"}), 404

        if lin.es_manual:
            if "agencia" in data:
                lin.agencia = (data.get("agencia") or "")[:120]
            if "ruta" in data:
                lin.ruta = (data.get("ruta") or "")[:200]

        for campo, maxlen in (
            ("matricula", 50),
            ("hora_llegada", 10),
            ("fin_descarga", 10),
            ("pallets", 50),
            ("personas", 200),
        ):
            if campo in data:
                setattr(lin, campo, (data.get(campo) or "")[:maxlen])

        lin.usuario_mod = current_user.username if current_user.is_authenticated else ""
        lin.fecha_mod = datetime.now()
        db.session.commit()
        return jsonify({"ok": True, "linea": _linea_dict(lin)})

    @app.route("/api/llegadas-camiones/linea/manual", methods=["POST"])
    @login_required
    def api_llegadas_linea_manual():
        data = request.get_json(silent=True) or {}
        fecha = _parse_fecha(data.get("fecha"))
        if not fecha:
            return jsonify({"ok": False, "error": "Fecha no válida"}), 400

        dia, lineas = _obtener_o_crear_dia(fecha)
        max_orden = max((l.orden for l in lineas), default=0)
        username = current_user.username if current_user.is_authenticated else ""
        lin = LlegadaCamionLinea(
            dia_id=dia.id,
            orden=max_orden + 1,
            agencia=(data.get("agencia") or "")[:120],
            ruta=(data.get("ruta") or "")[:200],
            matricula=(data.get("matricula") or "")[:50],
            hora_llegada=(data.get("hora_llegada") or "")[:10],
            fin_descarga=(data.get("fin_descarga") or "")[:10],
            pallets=(data.get("pallets") or "")[:50],
            personas=(data.get("personas") or "")[:200],
            es_manual=True,
            usuario_mod=username,
            fecha_mod=datetime.now(),
        )
        db.session.add(lin)
        db.session.commit()
        return jsonify({"ok": True, "linea": _linea_dict(lin)})

    @app.route("/api/llegadas-camiones/linea/<int:linea_id>", methods=["DELETE"])
    @login_required
    def api_llegadas_borrar_linea(linea_id):
        lin = db.session.query(LlegadaCamionLinea).filter_by(id=linea_id).first()
        if not lin:
            return jsonify({"ok": False, "error": "Línea no encontrada"}), 404
        if not lin.es_manual:
            return jsonify({"ok": False, "error": "Solo se pueden borrar rutas manuales"}), 400
        db.session.delete(lin)
        db.session.commit()
        return jsonify({"ok": True})

    @app.route("/api/llegadas-camiones/analisis")
    @login_required
    def api_llegadas_analisis():
        desde = _parse_fecha(request.args.get("desde"))
        hasta = _parse_fecha(request.args.get("hasta"))
        agencia = (request.args.get("agencia") or "").strip()
        ruta = (request.args.get("ruta") or "").strip()
        matricula = (request.args.get("matricula") or "").strip()

        q = (
            db.session.query(LlegadaCamionLinea, LlegadaCamionDia)
            .join(LlegadaCamionDia, LlegadaCamionLinea.dia_id == LlegadaCamionDia.id)
        )
        if desde:
            q = q.filter(LlegadaCamionDia.fecha >= desde)
        if hasta:
            q = q.filter(LlegadaCamionDia.fecha <= hasta)
        if agencia:
            q = q.filter(LlegadaCamionLinea.agencia.ilike(f"%{agencia}%"))
        if ruta:
            q = q.filter(LlegadaCamionLinea.ruta.ilike(f"%{ruta}%"))
        if matricula:
            q = q.filter(LlegadaCamionLinea.matricula.ilike(f"%{matricula}%"))

        filas = q.order_by(LlegadaCamionDia.fecha.desc(), LlegadaCamionLinea.orden).all()

        items = []
        por_agencia = Counter()
        rellenadas = 0
        for lin, dia in filas:
            tiene_dato = bool(
                (lin.matricula or "").strip()
                or (lin.hora_llegada or "").strip()
                or (lin.fin_descarga or "").strip()
                or (lin.pallets or "").strip()
                or (lin.personas or "").strip()
            )
            if tiene_dato:
                rellenadas += 1
                por_agencia[lin.agencia or "(sin agencia)"] += 1
            items.append({
                "fecha": dia.fecha.isoformat(),
                "turno": dia.turno or "",
                **_linea_dict(lin),
                "rellenada": tiene_dato,
            })

        return jsonify({
            "ok": True,
            "total": len(items),
            "rellenadas": rellenadas,
            "por_agencia": [
                {"agencia": k, "count": v}
                for k, v in sorted(por_agencia.items(), key=lambda x: (-x[1], x[0]))
            ],
            "items": items,
        })
