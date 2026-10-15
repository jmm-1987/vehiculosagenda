"""Documentos compartidos: categorías, filtro y vencimiento opcional."""
from __future__ import annotations

import os
import re
import uuid
from datetime import date, datetime

from flask import flash, redirect, render_template, request, send_file, url_for
from flask_login import current_user, login_required
from sqlalchemy import func, or_

import db
from models import DocPublicaCategoria, DocPublicaDocumento

REPO_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "documentacion_repositorio")
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


class DocumentacionError(Exception):
    pass


# Solo estos usuarios pueden editar o eliminar documentos.
_GESTORES = frozenset({"jmurillo", "pserrano", "rrodriguez"})


def _usuario() -> str:
    if getattr(current_user, "is_authenticated", False):
        return (current_user.username or "").strip()
    return ""


def _puede_gestionar() -> bool:
    return _usuario().lower() in _GESTORES


def _exigir_gestor() -> None:
    if not _puede_gestionar():
        raise DocumentacionError("No puedes editar ni eliminar documentos.")


def _entero(valor) -> int | None:
    try:
        numero = int(valor)
    except (TypeError, ValueError):
        return None
    return numero if numero > 0 else None


def _texto(valor, maximo: int) -> str:
    return " ".join((valor or "").split())[:maximo]


def _fecha(valor) -> date | None:
    texto = (valor or "").strip()
    if not texto:
        return None
    try:
        return datetime.strptime(texto, "%Y-%m-%d").date()
    except ValueError as exc:
        raise DocumentacionError("La fecha de vencimiento no es válida.") from exc


def _vencimiento_desde_form() -> date | None:
    if request.form.get("sin_vencimiento"):
        return None
    fecha = _fecha(request.form.get("vencimiento"))
    if fecha is None:
        raise DocumentacionError("Indica la fecha de vencimiento o marca Sin vencimiento.")
    return fecha


def _categoria(categoria_id: int | None) -> DocPublicaCategoria:
    if not categoria_id:
        raise DocumentacionError("Elige una categoría.")
    fila = db.session.query(DocPublicaCategoria).filter_by(id=categoria_id).first()
    if fila is None:
        raise DocumentacionError("La categoría no existe.")
    return fila


def _categoria_por_nombre(nombre: str) -> DocPublicaCategoria | None:
    return (
        db.session.query(DocPublicaCategoria)
        .filter(func.lower(DocPublicaCategoria.nombre) == nombre.lower())
        .first()
    )


def _titulo_desde_form() -> str:
    titulo = _texto(request.form.get("titulo"), 200)
    if len(titulo) < 2:
        raise DocumentacionError("El título tiene que tener al menos 2 caracteres.")
    return titulo


def _nombre_original(filename: str) -> tuple[str, str]:
    base = os.path.basename(filename or "").strip()
    if "." not in base:
        raise DocumentacionError("El archivo necesita una extensión: pdf, xls, xlsx, jpg, jpeg o png.")
    ext = base.rsplit(".", 1)[-1].lower()
    if ext not in EXTENSIONES:
        raise DocumentacionError("Solo se admiten pdf, xls, xlsx, jpg, jpeg y png.")
    visible = base.replace("\\", "_").replace("/", "_").replace('"', "")[:300]
    return visible, ext


def _leer_subida(archivo) -> tuple[bytes, str, str]:
    if archivo is None or not getattr(archivo, "filename", ""):
        raise DocumentacionError("Elige un archivo.")
    visible, ext = _nombre_original(archivo.filename)
    data = archivo.read(_MAX_BYTES + 1)
    if not data:
        raise DocumentacionError("El archivo está vacío.")
    if len(data) > _MAX_BYTES:
        raise DocumentacionError("El archivo supera los 20 MB.")
    return data, ext, visible


def _ruta_archivo(nombre: str) -> str:
    if not nombre or not _ARCHIVO_RE.fullmatch(nombre):
        raise DocumentacionError("El archivo guardado no es válido.")
    return os.path.join(REPO_DIR, nombre)


def _escribir(nombre: str, data: bytes) -> None:
    ruta = _ruta_archivo(nombre)
    with open(ruta, "wb") as salida:
        salida.write(data)


def _borrar_archivo(nombre: str) -> None:
    if not nombre:
        return
    try:
        ruta = _ruta_archivo(nombre)
    except DocumentacionError:
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
        "documentacion_publica",
        categoria=request.form.get("volver_categoria", ""),
        estado=estado,
    ))


def _pagina_categorias():
    return redirect(url_for("documentacion_publica_categorias"))


def _datos_categorias():
    categorias = db.session.query(DocPublicaCategoria).order_by(DocPublicaCategoria.nombre).all()
    conteo = dict(
        db.session.query(DocPublicaDocumento.categoria_id, func.count(DocPublicaDocumento.id))
        .group_by(DocPublicaDocumento.categoria_id)
        .all()
    )
    return categorias, conteo


def _fallo(exc: Exception, categorias: bool = False):
    db.session.rollback()
    if isinstance(exc, DocumentacionError):
        flash(str(exc))
    else:
        flash("No se ha podido completar la operación.")
    return _pagina_categorias() if categorias else _volver()


def register_documentacion_routes(app):

    @app.route("/documentacion-publica")
    @login_required
    def documentacion_publica():
        categoria_id = _entero(request.args.get("categoria"))
        estado = request.args.get("estado") or ""
        if estado not in _ESTADOS:
            estado = ""
        hoy = date.today()
        consulta = db.session.query(DocPublicaDocumento)
        if categoria_id:
            consulta = consulta.filter(DocPublicaDocumento.categoria_id == categoria_id)
        if estado == "vencidos":
            consulta = consulta.filter(
                DocPublicaDocumento.vencimiento.isnot(None),
                DocPublicaDocumento.vencimiento < hoy,
            )
        elif estado == "vigentes":
            consulta = consulta.filter(or_(
                DocPublicaDocumento.vencimiento.is_(None),
                DocPublicaDocumento.vencimiento >= hoy,
            ))
        elif estado == "sin":
            consulta = consulta.filter(DocPublicaDocumento.vencimiento.is_(None))
        documentos = consulta.order_by(
            DocPublicaDocumento.fecha_subida.desc(),
            DocPublicaDocumento.id.desc(),
        ).all()
        categorias, conteo = _datos_categorias()
        nombres = {cat.id: cat.nombre for cat in categorias}
        filas = []
        for doc in documentos:
            clase, texto = _estado_vencimiento(doc.vencimiento, hoy)
            filas.append({
                "doc": doc,
                "categoria": nombres.get(doc.categoria_id, "Sin categoría"),
                "clase": clase,
                "vencimiento": texto,
                "subida": doc.fecha_subida.strftime("%d/%m/%Y %H:%M") if doc.fecha_subida else "",
            })
        return render_template(
            "documentacion_publica.html",
            filas=filas,
            categorias=categorias,
            conteo=conteo,
            filtro_categoria=str(categoria_id or ""),
            filtro_estado=estado,
            total=len(filas),
            vencidos=sum(1 for fila in filas if fila["clase"] == "vencido"),
            puede_gestionar=_puede_gestionar(),
        )

    @app.route("/documentacion-publica/categoria", methods=["POST"])
    @login_required
    def documentacion_publica_categoria():
        try:
            nombre = _texto(request.form.get("nombre"), 80)
            if len(nombre) < 2:
                raise DocumentacionError("La categoría tiene que tener al menos 2 caracteres.")
            if _categoria_por_nombre(nombre):
                raise DocumentacionError(f"Ya existe la categoría «{nombre}».")
            db.session.add(DocPublicaCategoria(nombre=nombre))
            db.session.commit()
            flash(f"Categoría «{nombre}» creada.")
            return _pagina_categorias()
        except Exception as exc:
            return _fallo(exc, categorias=True)

    @app.route("/documentacion-publica/categoria/renombrar", methods=["POST"])
    @login_required
    def documentacion_publica_categoria_renombrar():
        try:
            fila = _categoria(_entero(request.form.get("id")))
            nombre = _texto(request.form.get("nombre"), 80)
            if len(nombre) < 2:
                raise DocumentacionError("La categoría tiene que tener al menos 2 caracteres.")
            otra = _categoria_por_nombre(nombre)
            if otra is not None and otra.id != fila.id:
                raise DocumentacionError(f"Ya existe la categoría «{nombre}».")
            fila.nombre = nombre
            db.session.commit()
            flash("Categoría actualizada.")
            return _pagina_categorias()
        except Exception as exc:
            return _fallo(exc, categorias=True)

    @app.route("/documentacion-publica/categoria/borrar", methods=["POST"])
    @login_required
    def documentacion_publica_categoria_borrar():
        try:
            fila = _categoria(_entero(request.form.get("id")))
            usados = db.session.query(DocPublicaDocumento).filter_by(categoria_id=fila.id).count()
            if usados:
                raise DocumentacionError("Esta categoría tiene documentos. Cámbialos de categoría antes de quitarla.")
            db.session.delete(fila)
            db.session.commit()
            flash("Categoría quitada.")
            return _pagina_categorias()
        except Exception as exc:
            return _fallo(exc, categorias=True)

    @app.route("/documentacion-publica/categorias")
    @login_required
    def documentacion_publica_categorias():
        categorias, conteo = _datos_categorias()
        return render_template(
            "documentacion_categorias.html",
            categorias=categorias,
            conteo=conteo,
        )

    @app.route("/documentacion-publica/subir", methods=["POST"])
    @login_required
    def documentacion_publica_subir():
        escrito = None
        try:
            titulo = _titulo_desde_form()
            categoria = _categoria(_entero(request.form.get("categoria_id")))
            vencimiento = _vencimiento_desde_form()
            data, ext, original = _leer_subida(request.files.get("archivo"))
            escrito = f"{uuid.uuid4().hex}.{ext}"
            _escribir(escrito, data)
            db.session.add(DocPublicaDocumento(
                categoria_id=categoria.id,
                titulo=titulo,
                nombre_original=original,
                nombre_archivo=escrito,
                vencimiento=vencimiento,
                usuario=_usuario(),
                fecha_subida=datetime.now(),
            ))
            db.session.commit()
            flash("Documento subido.")
            return _volver()
        except Exception as exc:
            if escrito:
                _borrar_archivo(escrito)
            return _fallo(exc)

    @app.route("/documentacion-publica/editar/<int:doc_id>", methods=["POST"])
    @login_required
    def documentacion_publica_editar(doc_id):
        escrito = None
        anterior = None
        try:
            _exigir_gestor()
            doc = db.session.query(DocPublicaDocumento).filter_by(id=doc_id).first()
            if doc is None:
                raise DocumentacionError("El documento no existe.")
            doc.titulo = _titulo_desde_form()
            doc.categoria_id = _categoria(_entero(request.form.get("categoria_id"))).id
            doc.vencimiento = _vencimiento_desde_form()
            archivo = request.files.get("archivo")
            if archivo is not None and archivo.filename:
                data, ext, original = _leer_subida(archivo)
                escrito = f"{uuid.uuid4().hex}.{ext}"
                _escribir(escrito, data)
                anterior = doc.nombre_archivo
                doc.nombre_archivo = escrito
                doc.nombre_original = original
            db.session.commit()
            flash("Documento actualizado.")
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

    @app.route("/documentacion-publica/borrar/<int:doc_id>", methods=["POST"])
    @login_required
    def documentacion_publica_borrar(doc_id):
        try:
            _exigir_gestor()
            doc = db.session.query(DocPublicaDocumento).filter_by(id=doc_id).first()
            if doc is None:
                raise DocumentacionError("El documento no existe.")
            nombre = doc.nombre_archivo
            db.session.delete(doc)
            db.session.commit()
            try:
                _borrar_archivo(nombre)
            except OSError:
                pass
            flash("Documento quitado.")
            return _volver()
        except Exception as exc:
            return _fallo(exc)

    @app.route("/documentacion-publica/archivo/<int:doc_id>")
    @login_required
    def documentacion_publica_archivo(doc_id):
        doc = db.session.query(DocPublicaDocumento).filter_by(id=doc_id).first()
        if doc is None:
            flash("El documento no existe.")
            return redirect(url_for("documentacion_publica"))
        try:
            ruta = _ruta_archivo(doc.nombre_archivo)
        except DocumentacionError:
            flash("El archivo guardado no es válido.")
            return redirect(url_for("documentacion_publica"))
        if not os.path.isfile(ruta):
            flash("No se encuentra el archivo en el servidor.")
            return redirect(url_for("documentacion_publica"))
        ext = doc.nombre_archivo.rsplit(".", 1)[-1]
        descargar = request.args.get("descargar") == "1" or ext in ("xls", "xlsx")
        return send_file(
            ruta,
            mimetype=EXTENSIONES.get(ext, "application/octet-stream"),
            as_attachment=descargar,
            download_name=doc.nombre_original or f"documento.{ext}",
            max_age=0,
            conditional=False,
        )
