"""Registros de calidad: cliente, fecha, categoría y archivo."""
from __future__ import annotations

import os
import re
import uuid
from datetime import date, datetime
from functools import wraps

from flask import flash, redirect, render_template, request, send_file, url_for
from flask_login import current_user, login_required
from sqlalchemy import func, or_

import db
from models import CalidadCategoria, CalidadRegistro
from permisos import puede

REPO_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "calidad_repositorio")
os.makedirs(REPO_DIR, exist_ok=True)

EXTENSIONES = {
    "pdf": "application/pdf",
    "xls": "application/vnd.ms-excel",
    "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "png": "image/png",
}
_ARCHIVO_RE = re.compile(r"^[a-f0-9]{32}\.(pdf|xls|xlsx|jpg|jpeg|png)$")
_MAX_BYTES = 20 * 1024 * 1024
_ESTADOS = {"", "vigentes", "vencidos", "sin"}


class CalidadError(Exception):
    pass


def _usuario() -> str:
    if getattr(current_user, "is_authenticated", False):
        return (current_user.username or "").strip()
    return ""


def _solo_calidad(vista):
    @wraps(vista)
    @login_required
    def envuelta(*args, **kwargs):
        if not puede(_usuario(), "calidad"):
            return redirect(url_for("portada"))
        return vista(*args, **kwargs)
    return envuelta


def _entero(valor) -> int | None:
    try:
        numero = int(valor)
    except (TypeError, ValueError):
        return None
    return numero if numero > 0 else None


def _texto(valor, maximo: int) -> str:
    return " ".join((valor or "").split())[:maximo]


def _fecha(valor, mensaje: str) -> date | None:
    texto = (valor or "").strip()
    if not texto:
        return None
    try:
        return datetime.strptime(texto, "%Y-%m-%d").date()
    except ValueError as exc:
        raise CalidadError(mensaje) from exc


def _cliente_desde_form() -> str:
    cliente = _texto(request.form.get("cliente"), 200)
    if len(cliente) < 2:
        raise CalidadError("El cliente tiene que tener al menos 2 caracteres.")
    return cliente


def _fecha_registro() -> date:
    fecha = _fecha(request.form.get("fecha"), "La fecha del registro no es válida.")
    if fecha is None:
        raise CalidadError("Indica la fecha del registro.")
    return fecha


def _vencimiento_desde_form() -> date | None:
    if request.form.get("sin_vencimiento"):
        return None
    fecha = _fecha(request.form.get("vencimiento"), "La fecha de vencimiento no es válida.")
    if fecha is None:
        raise CalidadError("Indica la fecha de vencimiento o marca Sin vencimiento.")
    return fecha


def _categoria(categoria_id: int | None) -> CalidadCategoria:
    if not categoria_id:
        raise CalidadError("Elige una categoría.")
    fila = db.session.query(CalidadCategoria).filter_by(id=categoria_id).first()
    if fila is None:
        raise CalidadError("La categoría no existe.")
    return fila


def _categoria_por_nombre(nombre: str) -> CalidadCategoria | None:
    return (
        db.session.query(CalidadCategoria)
        .filter(func.lower(CalidadCategoria.nombre) == nombre.lower())
        .first()
    )


def _nombre_original(filename: str) -> tuple[str, str]:
    base = os.path.basename(filename or "").strip()
    if "." not in base:
        raise CalidadError("El archivo necesita una extensión: pdf, xls, xlsx, jpg, jpeg o png.")
    ext = base.rsplit(".", 1)[-1].lower()
    if ext not in EXTENSIONES:
        raise CalidadError("Solo se admiten pdf, xls, xlsx, jpg, jpeg y png.")
    visible = base.replace("\\", "_").replace("/", "_").replace('"', "")[:300]
    return visible, ext


def _leer_subida(archivo) -> tuple[bytes, str, str]:
    if archivo is None or not getattr(archivo, "filename", ""):
        raise CalidadError("Elige un archivo.")
    visible, ext = _nombre_original(archivo.filename)
    data = archivo.read(_MAX_BYTES + 1)
    if not data:
        raise CalidadError("El archivo está vacío.")
    if len(data) > _MAX_BYTES:
        raise CalidadError("El archivo supera los 20 MB.")
    return data, ext, visible


def _ruta_archivo(nombre: str) -> str:
    if not nombre or not _ARCHIVO_RE.fullmatch(nombre):
        raise CalidadError("El archivo guardado no es válido.")
    return os.path.join(REPO_DIR, nombre)


def _escribir(nombre: str, data: bytes) -> None:
    with open(_ruta_archivo(nombre), "wb") as salida:
        salida.write(data)


def _borrar_archivo(nombre: str) -> None:
    if not nombre:
        return
    try:
        ruta = _ruta_archivo(nombre)
    except CalidadError:
        return
    if os.path.isfile(ruta):
        os.remove(ruta)


def _estado_vencimiento(fecha: date | None, hoy: date) -> tuple[str, str]:
    if fecha is None:
        return "sin", "Sin vencimiento"
    if fecha < hoy:
        return "vencido", f"Vencido el {fecha.strftime('%d/%m/%Y')}"
    if fecha == hoy:
        return "hoy", "Vence hoy"
    return "ok", f"Vence el {fecha.strftime('%d/%m/%Y')}"


def _volver():
    estado = request.form.get("volver_estado", "")
    if estado not in _ESTADOS:
        estado = ""
    return redirect(url_for(
        "calidad",
        categoria=request.form.get("volver_categoria", ""),
        estado=estado,
        q=request.form.get("volver_q", ""),
    ))


def _pagina_categorias():
    return redirect(url_for("calidad_categorias"))


def _datos_categorias():
    categorias = db.session.query(CalidadCategoria).order_by(CalidadCategoria.nombre).all()
    conteo = dict(
        db.session.query(CalidadRegistro.categoria_id, func.count(CalidadRegistro.id))
        .group_by(CalidadRegistro.categoria_id)
        .all()
    )
    return categorias, conteo


def _fallo(exc: Exception, categorias: bool = False):
    db.session.rollback()
    if isinstance(exc, CalidadError):
        flash(str(exc))
    else:
        flash("No se ha podido completar la operación.")
    return _pagina_categorias() if categorias else _volver()


def register_calidad_routes(app):

    @app.route("/calidad")
    @_solo_calidad
    def calidad():
        categoria_id = _entero(request.args.get("categoria"))
        estado = request.args.get("estado") or ""
        if estado not in _ESTADOS:
            estado = ""
        q = _texto(request.args.get("q"), 200)
        hoy = date.today()
        consulta = db.session.query(CalidadRegistro)
        if categoria_id:
            consulta = consulta.filter(CalidadRegistro.categoria_id == categoria_id)
        if q:
            consulta = consulta.filter(func.lower(CalidadRegistro.cliente).contains(q.lower()))
        if estado == "vencidos":
            consulta = consulta.filter(
                CalidadRegistro.vencimiento.isnot(None),
                CalidadRegistro.vencimiento < hoy,
            )
        elif estado == "vigentes":
            consulta = consulta.filter(or_(
                CalidadRegistro.vencimiento.is_(None),
                CalidadRegistro.vencimiento >= hoy,
            ))
        elif estado == "sin":
            consulta = consulta.filter(CalidadRegistro.vencimiento.is_(None))
        registros = consulta.order_by(CalidadRegistro.fecha.desc(), CalidadRegistro.id.desc()).all()
        categorias, conteo = _datos_categorias()
        nombres = {cat.id: cat.nombre for cat in categorias}
        filas = []
        for reg in registros:
            clase, texto = _estado_vencimiento(reg.vencimiento, hoy)
            filas.append({
                "reg": reg,
                "categoria": nombres.get(reg.categoria_id, "Sin categoría"),
                "clase": clase,
                "vencimiento": texto,
                "fecha": reg.fecha.strftime("%d/%m/%Y") if reg.fecha else "",
                "subida": reg.fecha_subida.strftime("%d/%m/%Y %H:%M") if reg.fecha_subida else "",
            })
        return render_template(
            "calidad.html",
            filas=filas,
            categorias=categorias,
            conteo=conteo,
            filtro_categoria=str(categoria_id or ""),
            filtro_estado=estado,
            filtro_q=q,
            total=len(filas),
        )

    @app.route("/calidad/categorias")
    @_solo_calidad
    def calidad_categorias():
        categorias, conteo = _datos_categorias()
        return render_template("calidad_categorias.html", categorias=categorias, conteo=conteo)

    @app.route("/calidad/categoria", methods=["POST"])
    @_solo_calidad
    def calidad_categoria():
        try:
            nombre = _texto(request.form.get("nombre"), 80)
            if len(nombre) < 2:
                raise CalidadError("La categoría tiene que tener al menos 2 caracteres.")
            if _categoria_por_nombre(nombre):
                raise CalidadError(f"Ya existe la categoría «{nombre}».")
            db.session.add(CalidadCategoria(nombre=nombre))
            db.session.commit()
            flash(f"Categoría «{nombre}» creada.")
            return _pagina_categorias()
        except Exception as exc:
            return _fallo(exc, categorias=True)

    @app.route("/calidad/categoria/renombrar", methods=["POST"])
    @_solo_calidad
    def calidad_categoria_renombrar():
        try:
            fila = _categoria(_entero(request.form.get("id")))
            nombre = _texto(request.form.get("nombre"), 80)
            if len(nombre) < 2:
                raise CalidadError("La categoría tiene que tener al menos 2 caracteres.")
            otra = _categoria_por_nombre(nombre)
            if otra is not None and otra.id != fila.id:
                raise CalidadError(f"Ya existe la categoría «{nombre}».")
            fila.nombre = nombre
            db.session.commit()
            flash("Categoría actualizada.")
            return _pagina_categorias()
        except Exception as exc:
            return _fallo(exc, categorias=True)

    @app.route("/calidad/categoria/borrar", methods=["POST"])
    @_solo_calidad
    def calidad_categoria_borrar():
        try:
            fila = _categoria(_entero(request.form.get("id")))
            usados = db.session.query(CalidadRegistro).filter_by(categoria_id=fila.id).count()
            if usados:
                raise CalidadError("Esta categoría tiene registros. Cámbialos de categoría antes de quitarla.")
            db.session.delete(fila)
            db.session.commit()
            flash("Categoría quitada.")
            return _pagina_categorias()
        except Exception as exc:
            return _fallo(exc, categorias=True)

    @app.route("/calidad/subir", methods=["POST"])
    @_solo_calidad
    def calidad_subir():
        escrito = None
        try:
            cliente = _cliente_desde_form()
            fecha = _fecha_registro()
            categoria = _categoria(_entero(request.form.get("categoria_id")))
            vencimiento = _vencimiento_desde_form()
            data, ext, original = _leer_subida(request.files.get("archivo"))
            escrito = f"{uuid.uuid4().hex}.{ext}"
            _escribir(escrito, data)
            db.session.add(CalidadRegistro(
                categoria_id=categoria.id,
                cliente=cliente,
                fecha=fecha,
                nombre_original=original,
                nombre_archivo=escrito,
                vencimiento=vencimiento,
                usuario=_usuario(),
                fecha_subida=datetime.now(),
            ))
            db.session.commit()
            flash("Registro guardado.")
            return _volver()
        except Exception as exc:
            if escrito:
                _borrar_archivo(escrito)
            return _fallo(exc)

    @app.route("/calidad/editar/<int:reg_id>", methods=["POST"])
    @_solo_calidad
    def calidad_editar(reg_id):
        escrito = None
        anterior = None
        try:
            reg = db.session.query(CalidadRegistro).filter_by(id=reg_id).first()
            if reg is None:
                raise CalidadError("El registro no existe.")
            reg.cliente = _cliente_desde_form()
            reg.fecha = _fecha_registro()
            reg.categoria_id = _categoria(_entero(request.form.get("categoria_id"))).id
            reg.vencimiento = _vencimiento_desde_form()
            archivo = request.files.get("archivo")
            if archivo is not None and archivo.filename:
                data, ext, original = _leer_subida(archivo)
                escrito = f"{uuid.uuid4().hex}.{ext}"
                _escribir(escrito, data)
                anterior = reg.nombre_archivo
                reg.nombre_archivo = escrito
                reg.nombre_original = original
            db.session.commit()
            flash("Registro actualizado.")
        except Exception as exc:
            if escrito:
                _borrar_archivo(escrito)
            return _fallo(exc)
        if anterior and anterior != escrito:
            try:
                _borrar_archivo(anterior)
            except OSError:
                pass
        return _volver()

    @app.route("/calidad/borrar/<int:reg_id>", methods=["POST"])
    @_solo_calidad
    def calidad_borrar(reg_id):
        try:
            reg = db.session.query(CalidadRegistro).filter_by(id=reg_id).first()
            if reg is None:
                raise CalidadError("El registro no existe.")
            nombre = reg.nombre_archivo
            db.session.delete(reg)
            db.session.commit()
            try:
                _borrar_archivo(nombre)
            except OSError:
                pass
            flash("Registro quitado.")
            return _volver()
        except Exception as exc:
            return _fallo(exc)

    @app.route("/calidad/archivo/<int:reg_id>")
    @_solo_calidad
    def calidad_archivo(reg_id):
        reg = db.session.query(CalidadRegistro).filter_by(id=reg_id).first()
        if reg is None:
            flash("El registro no existe.")
            return redirect(url_for("calidad"))
        try:
            ruta = _ruta_archivo(reg.nombre_archivo)
        except CalidadError:
            flash("El archivo guardado no es válido.")
            return redirect(url_for("calidad"))
        if not os.path.isfile(ruta):
            flash("No se encuentra el archivo en el servidor.")
            return redirect(url_for("calidad"))
        ext = reg.nombre_archivo.rsplit(".", 1)[-1]
        descargar = request.args.get("descargar") == "1" or ext in ("xls", "xlsx")
        return send_file(
            ruta,
            mimetype=EXTENSIONES.get(ext, "application/octet-stream"),
            as_attachment=descargar,
            download_name=reg.nombre_original or f"registro.{ext}",
            max_age=0,
            conditional=False,
        )
