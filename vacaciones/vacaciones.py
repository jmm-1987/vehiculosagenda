"""Rutas del Control de Vacaciones y Ausencias 2026 (aislado del resto)."""
from __future__ import annotations

import os
import uuid
from datetime import datetime, date

from flask import render_template, abort, request, jsonify, send_file, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

import db
from models import VacacionesEmpleado, VacacionesAusencia

USUARIOS_VACACIONES = frozenset({"jmurillo", "javimurillo", "jamurillo", "rocio", "pserrano"})
UPLOAD_SUBDIR = "vacaciones"
ALLOWED_EXT = {".pdf", ".png", ".jpg", ".jpeg", ".webp", ".gif"}


def _usuario_ok():
    username = (current_user.username or "").strip().lower()
    return username in USUARIOS_VACACIONES


def _require_vacaciones():
    if not _usuario_ok():
        abort(403)


def _upload_dir():
    path = os.path.join(current_app.root_path, "static", "subidas", UPLOAD_SUBDIR)
    os.makedirs(path, exist_ok=True)
    return path


def _parse_fecha(val):
    if not val:
        return None
    try:
        return datetime.strptime(val, "%Y-%m-%d").date()
    except ValueError:
        return None


def _empleado(sede: str, nombre: str):
    return (
        db.session.query(VacacionesEmpleado)
        .filter_by(sede=sede, nombre=nombre)
        .first()
    )


def _empleado_dict(emp: VacacionesEmpleado):
    return {
        "id": emp.id,
        "sede": emp.sede,
        "name": emp.nombre,
        "nombre": emp.nombre,
        "dept": emp.departamento or "",
        "departamento": emp.departamento or "",
        "puesto": emp.puesto or "",
        "vac": emp.vac_asignadas if emp.vac_asignadas is not None else 30,
        "vac_asignadas": emp.vac_asignadas if emp.vac_asignadas is not None else 30,
        "active": bool(emp.activo),
        "activo": bool(emp.activo),
    }


def _ausencia_dict(a: VacacionesAusencia, emp: VacacionesEmpleado):
    return {
        "id": a.id,
        "empleado_id": emp.id,
        "empleado": emp.nombre,
        "sede": emp.sede,
        "fecha": a.fecha.isoformat(),
        "codigo": a.codigo,
        "nota": a.nota or "",
        "tiene_adjunto": bool(a.adjunto),
        "adjunto_nombre": a.adjunto_nombre or "",
        "usuario": a.usuario or "",
    }


def register_vacaciones_routes(app):
    @app.route("/vacaciones")
    @login_required
    def vacaciones():
        _require_vacaciones()
        return render_template("vacaciones.html")

    @app.route("/api/vacaciones/empleados")
    @login_required
    def api_vacaciones_empleados():
        _require_vacaciones()
        sede = (request.args.get("sede") or "").strip()
        if sede not in ("merida", "navalmoral"):
            return jsonify({"ok": False, "error": "Sede no válida"}), 400
        filas = (
            db.session.query(VacacionesEmpleado)
            .filter_by(sede=sede)
            .order_by(VacacionesEmpleado.nombre)
            .all()
        )
        return jsonify({"ok": True, "empleados": [_empleado_dict(e) for e in filas]})

    @app.route("/api/vacaciones/empleado", methods=["POST"])
    @login_required
    def api_vacaciones_guardar_empleado():
        """Alta o edición de empleado (nombre, dept, puesto, vac, activo)."""
        _require_vacaciones()
        data = request.get_json(silent=True) or {}
        sede = (data.get("sede") or "").strip()
        if sede not in ("merida", "navalmoral"):
            return jsonify({"ok": False, "error": "Sede no válida"}), 400

        emp_id = data.get("id")
        nombre = (data.get("nombre") or data.get("name") or "").strip().upper()
        if not nombre:
            return jsonify({"ok": False, "error": "El nombre es obligatorio"}), 400

        dept = (data.get("departamento") or data.get("dept") or "")[:100]
        puesto = (data.get("puesto") or "—")[:100]
        try:
            vac = int(data.get("vac") if data.get("vac") is not None else data.get("vac_asignadas") or 30)
        except (TypeError, ValueError):
            vac = 30
        activo = data.get("active", data.get("activo", True)) is not False

        emp = None
        if emp_id:
            emp = db.session.query(VacacionesEmpleado).filter_by(id=int(emp_id), sede=sede).first()

        # Evitar duplicar nombre en la misma sede
        otro = (
            db.session.query(VacacionesEmpleado)
            .filter_by(sede=sede, nombre=nombre)
            .first()
        )
        if otro and (not emp or otro.id != emp.id):
            return jsonify({"ok": False, "error": f'Ya existe "{nombre}" en esta sede'}), 400

        if not emp:
            emp = VacacionesEmpleado(
                sede=sede,
                nombre=nombre,
                departamento=dept,
                puesto=puesto,
                vac_asignadas=vac,
                activo=activo,
            )
            db.session.add(emp)
        else:
            emp.nombre = nombre
            emp.departamento = dept
            emp.puesto = puesto
            emp.vac_asignadas = vac
            emp.activo = activo

        db.session.commit()
        return jsonify({"ok": True, "empleado": _empleado_dict(emp)})

    @app.route("/api/vacaciones/sync-empleados", methods=["POST"])
    @login_required
    def api_vacaciones_sync_empleados():
        """Siembra inicial: solo crea empleados que aún no existen en la sede."""
        _require_vacaciones()
        data = request.get_json(silent=True) or {}
        sede = (data.get("sede") or "").strip()
        empleados = data.get("empleados") or []
        if sede not in ("merida", "navalmoral"):
            return jsonify({"ok": False, "error": "Sede no válida"}), 400

        creados = 0
        for item in empleados:
            nombre = (item.get("nombre") or item.get("name") or "").strip().upper()
            if not nombre:
                continue
            emp = _empleado(sede, nombre)
            if emp:
                continue
            emp = VacacionesEmpleado(
                sede=sede,
                nombre=nombre,
                departamento=(item.get("departamento") or item.get("dept") or "")[:100],
                puesto=(item.get("puesto") or "")[:100],
                vac_asignadas=int(item.get("vac") or item.get("vac_asignadas") or 30),
                activo=item.get("active", True) is not False,
            )
            db.session.add(emp)
            creados += 1
        db.session.commit()
        return jsonify({"ok": True, "creados": creados})

    @app.route("/api/vacaciones/ausencias")
    @login_required
    def api_vacaciones_ausencias():
        _require_vacaciones()
        sede = (request.args.get("sede") or "").strip()
        anio = int(request.args.get("anio") or 2026)
        if sede not in ("merida", "navalmoral"):
            return jsonify({"ok": False, "error": "Sede no válida"}), 400

        empleados = db.session.query(VacacionesEmpleado).filter_by(sede=sede).all()
        emp_by_id = {e.id: e for e in empleados}
        if not emp_by_id:
            return jsonify({"ok": True, "ausencias": []})

        inicio = date(anio, 1, 1)
        fin = date(anio, 12, 31)
        filas = (
            db.session.query(VacacionesAusencia)
            .filter(
                VacacionesAusencia.empleado_id.in_(list(emp_by_id.keys())),
                VacacionesAusencia.fecha >= inicio,
                VacacionesAusencia.fecha <= fin,
            )
            .all()
        )
        return jsonify({
            "ok": True,
            "ausencias": [
                _ausencia_dict(a, emp_by_id[a.empleado_id])
                for a in filas
                if a.empleado_id in emp_by_id
            ],
        })

    @app.route("/api/vacaciones/ausencia", methods=["POST"])
    @login_required
    def api_vacaciones_guardar_ausencia():
        _require_vacaciones()
        data = request.get_json(silent=True) or {}
        sede = (data.get("sede") or "").strip()
        nombre = (data.get("empleado") or "").strip().upper()
        codigo = (data.get("codigo") or "").strip().upper()
        fecha = _parse_fecha(data.get("fecha"))
        nota = (data.get("nota") or "")[:1000]

        if sede not in ("merida", "navalmoral") or not nombre or not fecha:
            return jsonify({"ok": False, "error": "Datos incompletos"}), 400

        emp = _empleado(sede, nombre)
        if not emp:
            emp = VacacionesEmpleado(
                sede=sede,
                nombre=nombre,
                departamento=(data.get("departamento") or "")[:100],
                puesto=(data.get("puesto") or "")[:100],
                vac_asignadas=30,
                activo=True,
            )
            db.session.add(emp)
            db.session.flush()

        if not codigo:
            existente = (
                db.session.query(VacacionesAusencia)
                .filter_by(empleado_id=emp.id, fecha=fecha)
                .first()
            )
            if existente:
                if existente.adjunto:
                    path = os.path.join(_upload_dir(), existente.adjunto)
                    if os.path.isfile(path):
                        try:
                            os.remove(path)
                        except OSError:
                            pass
                db.session.delete(existente)
                db.session.commit()
            return jsonify({"ok": True, "borrada": True})

        ausencia = (
            db.session.query(VacacionesAusencia)
            .filter_by(empleado_id=emp.id, fecha=fecha)
            .first()
        )
        if not ausencia:
            ausencia = VacacionesAusencia(
                empleado_id=emp.id,
                fecha=fecha,
                codigo=codigo,
                nota=nota,
                usuario=current_user.username if current_user.is_authenticated else "",
                fecha_registro=datetime.now(),
            )
            db.session.add(ausencia)
        else:
            ausencia.codigo = codigo
            if "nota" in data:
                ausencia.nota = nota
            ausencia.usuario = current_user.username if current_user.is_authenticated else ""
            ausencia.fecha_registro = datetime.now()
        db.session.commit()
        return jsonify({"ok": True, "ausencia": _ausencia_dict(ausencia, emp)})

    @app.route("/api/vacaciones/ausencia/adjunto", methods=["POST"])
    @login_required
    def api_vacaciones_adjunto():
        _require_vacaciones()
        sede = (request.form.get("sede") or "").strip()
        nombre = (request.form.get("empleado") or "").strip().upper()
        fecha = _parse_fecha(request.form.get("fecha"))
        fichero = request.files.get("adjunto")

        if sede not in ("merida", "navalmoral") or not nombre or not fecha or not fichero:
            return jsonify({"ok": False, "error": "Datos incompletos"}), 400

        emp = _empleado(sede, nombre)
        if not emp:
            return jsonify({"ok": False, "error": "Empleado no encontrado"}), 404

        ausencia = (
            db.session.query(VacacionesAusencia)
            .filter_by(empleado_id=emp.id, fecha=fecha)
            .first()
        )
        if not ausencia:
            return jsonify({"ok": False, "error": "Primero registra la ausencia del día"}), 400

        original = secure_filename(fichero.filename or "adjunto")
        ext = os.path.splitext(original)[1].lower()
        if ext not in ALLOWED_EXT:
            return jsonify({
                "ok": False,
                "error": "Solo PDF o imágenes (png, jpg, jpeg, webp, gif)",
            }), 400

        stored = f"{emp.id}_{fecha.isoformat()}_{uuid.uuid4().hex[:8]}{ext}"
        dest = os.path.join(_upload_dir(), stored)

        if ausencia.adjunto:
            old = os.path.join(_upload_dir(), ausencia.adjunto)
            if os.path.isfile(old):
                try:
                    os.remove(old)
                except OSError:
                    pass

        fichero.save(dest)
        ausencia.adjunto = stored
        ausencia.adjunto_nombre = original
        ausencia.usuario = current_user.username if current_user.is_authenticated else ""
        ausencia.fecha_registro = datetime.now()
        db.session.commit()
        return jsonify({"ok": True, "ausencia": _ausencia_dict(ausencia, emp)})

    @app.route("/api/vacaciones/adjunto/<int:ausencia_id>")
    @login_required
    def api_vacaciones_descargar_adjunto(ausencia_id):
        _require_vacaciones()
        ausencia = db.session.query(VacacionesAusencia).filter_by(id=ausencia_id).first()
        if not ausencia or not ausencia.adjunto:
            return "Adjunto no encontrado", 404
        path = os.path.join(_upload_dir(), ausencia.adjunto)
        if not os.path.isfile(path):
            return "Fichero no encontrado", 404
        return send_file(
            path,
            as_attachment=True,
            download_name=ausencia.adjunto_nombre or ausencia.adjunto,
        )

    @app.route("/api/vacaciones/empleado/<int:empleado_id>/ausencias")
    @login_required
    def api_vacaciones_empleado_ausencias(empleado_id):
        _require_vacaciones()
        emp = db.session.query(VacacionesEmpleado).filter_by(id=empleado_id).first()
        if not emp:
            return jsonify({"ok": False, "error": "Empleado no encontrado"}), 404
        filas = (
            db.session.query(VacacionesAusencia)
            .filter_by(empleado_id=emp.id)
            .order_by(VacacionesAusencia.fecha.desc())
            .all()
        )
        return jsonify({
            "ok": True,
            "empleado": {
                "id": emp.id,
                "nombre": emp.nombre,
                "sede": emp.sede,
                "departamento": emp.departamento,
                "puesto": emp.puesto,
                "vac_asignadas": emp.vac_asignadas,
            },
            "ausencias": [_ausencia_dict(a, emp) for a in filas],
        })
