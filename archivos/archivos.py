"""Tarifa Alditraex y KPIs: documentos por año, en carpetas y subcarpetas."""
from __future__ import annotations

import os
import re
import uuid
from datetime import date, datetime

from flask import flash, redirect, render_template, request, send_file, url_for
from flask_login import current_user, login_required
from sqlalchemy import func

import db
from models import RepositorioCarpeta, RepositorioDocumento

REPO_BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "repositorios")
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
_PROFUNDIDAD = 8
_GESTORES = frozenset({"jmurillo", "pserrano", "rrodriguez"})

REPOSITORIOS = (
    {
        "ambito": "tarifa",
        "slug": "tarifa-alditraex",
        "endpoint": "tarifa_alditraex",
        "titulo": "Tarifa Alditraex",
        "subtitulo": "Elige el año, crea carpetas y subcarpetas y guarda ahí las tarifas. Cualquier usuario puede verlas y subirlas.",
    },
    {
        "ambito": "kpis",
        "slug": "kpis",
        "endpoint": "kpis",
        "titulo": "KPIs",
        "subtitulo": "Elige el año, crea carpetas y subcarpetas y guarda ahí los indicadores. Cualquier usuario puede verlos y subirlos.",
    },
)


class RepoError(Exception):
    pass


def _usuario() -> str:
    if getattr(current_user, "is_authenticated", False):
        return (current_user.username or "").strip()
    return ""


def _puede_gestionar() -> bool:
    return _usuario().lower() in _GESTORES


def _exigir_gestor() -> None:
    if not _puede_gestionar():
        raise RepoError("No puedes editar ni eliminar documentos.")


def _texto(valor, maximo: int) -> str:
    return " ".join((valor or "").split())[:maximo]


def _entero(valor) -> int | None:
    try:
        numero = int(valor)
    except (TypeError, ValueError):
        return None
    return numero if numero > 0 else None


def _anio_valido(valor, por_defecto: int | None = None) -> int:
    if por_defecto is None:
        por_defecto = date.today().year
    try:
        anio = int(str(valor).strip())
    except (TypeError, ValueError):
        return por_defecto
    if anio < 2000 or anio > 2100:
        return por_defecto
    return anio


def _anio_form() -> int:
    try:
        anio = int(str(request.form.get("anio") or "").strip())
    except (TypeError, ValueError) as exc:
        raise RepoError("El año no es válido.") from exc
    if anio < 2000 or anio > 2100:
        raise RepoError("El año tiene que estar entre 2000 y 2100.")
    return anio


def _directorio(ambito: str) -> str:
    ruta = os.path.join(REPO_BASE, ambito)
    os.makedirs(ruta, exist_ok=True)
    return ruta


def _ruta_archivo(ambito: str, nombre: str) -> str:
    if not nombre or not _ARCHIVO_RE.fullmatch(nombre):
        raise RepoError("El archivo guardado no es válido.")
    return os.path.join(_directorio(ambito), nombre)


def _escribir(ambito: str, nombre: str, data: bytes) -> None:
    try:
        ruta = _ruta_archivo(ambito, nombre)
        with open(ruta, "wb") as salida:
            salida.write(data)
    except OSError as exc:
        raise RepoError("No se ha podido guardar el archivo. Revisa los permisos de la carpeta repositorios.") from exc


def _borrar_archivo(ambito: str, nombre: str) -> None:
    if not nombre:
        return
    try:
        ruta = _ruta_archivo(ambito, nombre)
    except RepoError:
        return
    if os.path.isfile(ruta):
        os.remove(ruta)


def _nombre_original(filename: str) -> tuple[str, str]:
    base = os.path.basename(filename or "").strip()
    if "." not in base:
        raise RepoError("El archivo necesita una extensión: pdf, xls, xlsx, jpg, jpeg o png.")
    ext = base.rsplit(".", 1)[-1].lower()
    if ext not in EXTENSIONES:
        raise RepoError("Solo se admiten pdf, xls, xlsx, jpg, jpeg y png.")
    visible = base.replace("\\", "_").replace("/", "_").replace('"', "")[:300]
    return visible, ext


def _leer_subida(archivo) -> tuple[bytes, str, str]:
    if archivo is None or not getattr(archivo, "filename", ""):
        raise RepoError("Elige un archivo.")
    visible, ext = _nombre_original(archivo.filename)
    data = archivo.read(_MAX_BYTES + 1)
    if not data:
        raise RepoError("El archivo está vacío.")
    if len(data) > _MAX_BYTES:
        raise RepoError("El archivo supera los 20 MB.")
    return data, ext, visible


def _titulo() -> str:
    titulo = _texto(request.form.get("titulo"), 200)
    if len(titulo) < 2:
        raise RepoError("El título tiene que tener al menos 2 caracteres.")
    return titulo


def _nombre_carpeta() -> str:
    nombre = _texto(request.form.get("nombre"), 120)
    if len(nombre) < 2:
        raise RepoError("El nombre de la carpeta tiene que tener al menos 2 caracteres.")
    return nombre


def _carpeta(ambito: str, carpeta_id: int | None) -> RepositorioCarpeta | None:
    if not carpeta_id:
        return None
    fila = db.session.query(RepositorioCarpeta).filter_by(id=carpeta_id, ambito=ambito).first()
    if fila is None:
        raise RepoError("La carpeta no existe.")
    return fila


def _cadena(carpeta: RepositorioCarpeta | None) -> list[RepositorioCarpeta]:
    if carpeta is None:
        return []
    cadena = []
    visto = set()
    actual = carpeta
    while actual is not None and actual.id not in visto:
        visto.add(actual.id)
        cadena.append(actual)
        if not actual.padre_id:
            break
        actual = (
            db.session.query(RepositorioCarpeta)
            .filter_by(id=actual.padre_id, ambito=carpeta.ambito, anio=carpeta.anio)
            .first()
        )
    cadena.reverse()
    return cadena


def _hermana(ambito: str, anio: int, padre_id: int | None, nombre: str, excluir: int | None = None):
    consulta = db.session.query(RepositorioCarpeta).filter(
        RepositorioCarpeta.ambito == ambito,
        RepositorioCarpeta.anio == anio,
        func.lower(RepositorioCarpeta.nombre) == nombre.lower(),
    )
    if padre_id is None:
        consulta = consulta.filter(RepositorioCarpeta.padre_id.is_(None))
    else:
        consulta = consulta.filter(RepositorioCarpeta.padre_id == padre_id)
    if excluir:
        consulta = consulta.filter(RepositorioCarpeta.id != excluir)
    return consulta.first()


def _anios(ambito: str, seleccionado: int) -> list[int]:
    guardados = [
        anio
        for (anio,) in db.session.query(RepositorioCarpeta.anio).filter_by(ambito=ambito).distinct()
        if anio
    ]
    hoy = date.today().year
    inicio = max(2000, min([hoy - 4, seleccionado, *guardados] or [hoy]))
    fin = min(2100, max([hoy + 1, seleccionado, *guardados] or [hoy]))
    return list(range(fin, inicio - 1, -1))


def _hijos(ambito: str, anio: int, padre_id: int | None) -> list[RepositorioCarpeta]:
    consulta = db.session.query(RepositorioCarpeta).filter_by(ambito=ambito, anio=anio)
    if padre_id is None:
        consulta = consulta.filter(RepositorioCarpeta.padre_id.is_(None))
    else:
        consulta = consulta.filter_by(padre_id=padre_id)
    return consulta.order_by(func.lower(RepositorioCarpeta.nombre), RepositorioCarpeta.id).all()


def _conteos(ids: list[int]) -> tuple[dict, dict]:
    if not ids:
        return {}, {}
    docs = dict(
        db.session.query(RepositorioDocumento.carpeta_id, func.count(RepositorioDocumento.id))
        .filter(RepositorioDocumento.carpeta_id.in_(ids))
        .group_by(RepositorioDocumento.carpeta_id)
        .all()
    )
    hijos = dict(
        db.session.query(RepositorioCarpeta.padre_id, func.count(RepositorioCarpeta.id))
        .filter(RepositorioCarpeta.padre_id.in_(ids))
        .group_by(RepositorioCarpeta.padre_id)
        .all()
    )
    return docs, hijos


def _documentos(carpeta_id: int) -> list[RepositorioDocumento]:
    return (
        db.session.query(RepositorioDocumento)
        .filter_by(carpeta_id=carpeta_id)
        .order_by(RepositorioDocumento.fecha_subida.desc(), RepositorioDocumento.id.desc())
        .all()
    )


def _volver(endpoint: str):
    anio = _anio_valido(request.form.get("volver_anio") or request.form.get("anio"))
    carpeta = _entero(request.form.get("volver_carpeta") or request.form.get("carpeta"))
    return redirect(url_for(endpoint, anio=anio, carpeta=carpeta or ""))


def _fallo(endpoint: str, exc: Exception):
    db.session.rollback()
    if isinstance(exc, RepoError):
        flash(str(exc))
    else:
        flash("No se ha podido completar la operación.")
    return _volver(endpoint)


def _rutas(cfg: dict) -> dict:
    base = cfg["endpoint"]
    return {
        "inicio": base,
        "carpeta": base + "_carpeta",
        "renombrar": base + "_renombrar",
        "borrar_carpeta": base + "_borrar_carpeta",
        "subir": base + "_subir",
        "editar": base + "_editar",
        "borrar": base + "_borrar",
        "archivo": base + "_archivo",
    }


def register_repositorio_routes(app):
    for cfg in REPOSITORIOS:
        try:
            _directorio(cfg["ambito"])
        except OSError:
            pass
        _montar(app, cfg)


def _montar(app, cfg: dict):
    ambito = cfg["ambito"]
    slug = cfg["slug"]
    ep = cfg["endpoint"]
    rutas = _rutas(cfg)

    @app.route(f"/{slug}", endpoint=ep)
    @login_required
    def inicio():
        anio = _anio_valido(request.args.get("anio"))
        try:
            carpeta = _carpeta(ambito, _entero(request.args.get("carpeta")))
        except RepoError as exc:
            flash(str(exc))
            return redirect(url_for(ep, anio=anio))
        if carpeta is not None and carpeta.anio != anio:
            return redirect(url_for(ep, anio=carpeta.anio, carpeta=carpeta.id))
        cadena = _cadena(carpeta)
        if len(cadena) > _PROFUNDIDAD:
            flash("Esta carpeta está demasiado anidada.")
            return redirect(url_for(ep, anio=anio))
        padre_id = carpeta.id if carpeta else None
        carpetas = _hijos(ambito, anio, padre_id)
        docs_n, hijos_n = _conteos([c.id for c in carpetas])
        documentos = _documentos(carpeta.id) if carpeta else []
        return render_template(
            "repositorio.html",
            titulo=cfg["titulo"],
            subtitulo=cfg["subtitulo"],
            rutas=rutas,
            anio=anio,
            anios=_anios(ambito, anio),
            carpeta=carpeta,
            cadena=cadena,
            carpetas=carpetas,
            docs_n=docs_n,
            hijos_n=hijos_n,
            documentos=documentos,
            puede_gestionar=_puede_gestionar(),
        )

    @app.route(f"/{slug}/carpeta", methods=["POST"], endpoint=rutas["carpeta"])
    @login_required
    def crear_carpeta():
        try:
            anio = _anio_form()
            padre = _carpeta(ambito, _entero(request.form.get("padre_id")))
            if padre is not None and padre.anio != anio:
                raise RepoError("La carpeta no pertenece a ese año.")
            if len(_cadena(padre)) >= _PROFUNDIDAD:
                raise RepoError("No se pueden crear más niveles de subcarpetas.")
            nombre = _nombre_carpeta()
            padre_id = padre.id if padre else None
            if _hermana(ambito, anio, padre_id, nombre):
                raise RepoError(f"Ya existe la carpeta «{nombre}».")
            db.session.add(RepositorioCarpeta(
                ambito=ambito,
                anio=anio,
                padre_id=padre_id,
                nombre=nombre,
            ))
            db.session.commit()
            flash(f"Carpeta «{nombre}» creada.")
            return _volver(ep)
        except Exception as exc:
            return _fallo(ep, exc)

    @app.route(f"/{slug}/carpeta/renombrar", methods=["POST"], endpoint=rutas["renombrar"])
    @login_required
    def renombrar_carpeta():
        try:
            fila = _carpeta(ambito, _entero(request.form.get("id")))
            if fila is None:
                raise RepoError("La carpeta no existe.")
            nombre = _nombre_carpeta()
            if _hermana(ambito, fila.anio, fila.padre_id, nombre, excluir=fila.id):
                raise RepoError(f"Ya existe la carpeta «{nombre}».")
            fila.nombre = nombre
            db.session.commit()
            flash("Carpeta actualizada.")
            return _volver(ep)
        except Exception as exc:
            return _fallo(ep, exc)

    @app.route(f"/{slug}/carpeta/borrar", methods=["POST"], endpoint=rutas["borrar_carpeta"])
    @login_required
    def borrar_carpeta():
        try:
            fila = _carpeta(ambito, _entero(request.form.get("id")))
            if fila is None:
                raise RepoError("La carpeta no existe.")
            if db.session.query(RepositorioCarpeta).filter_by(padre_id=fila.id).count():
                raise RepoError("Esta carpeta tiene subcarpetas. Vacía las de dentro antes de quitarla.")
            if db.session.query(RepositorioDocumento).filter_by(carpeta_id=fila.id).count():
                raise RepoError("Esta carpeta tiene documentos. Quítalos antes de borrar la carpeta.")
            db.session.delete(fila)
            db.session.commit()
            flash("Carpeta quitada.")
            return _volver(ep)
        except Exception as exc:
            return _fallo(ep, exc)

    @app.route(f"/{slug}/subir", methods=["POST"], endpoint=rutas["subir"])
    @login_required
    def subir():
        escrito = None
        try:
            carpeta = _carpeta(ambito, _entero(request.form.get("carpeta_id")))
            if carpeta is None:
                raise RepoError("Entra en una carpeta para subir el documento.")
            titulo = _titulo()
            data, ext, original = _leer_subida(request.files.get("archivo"))
            escrito = f"{uuid.uuid4().hex}.{ext}"
            _escribir(ambito, escrito, data)
            db.session.add(RepositorioDocumento(
                carpeta_id=carpeta.id,
                titulo=titulo,
                nombre_original=original,
                nombre_archivo=escrito,
                usuario=_usuario(),
                fecha_subida=datetime.now(),
            ))
            db.session.commit()
            flash("Documento subido.")
            return _volver(ep)
        except Exception as exc:
            if escrito:
                _borrar_archivo(ambito, escrito)
            return _fallo(ep, exc)

    @app.route(f"/{slug}/editar/<int:doc_id>", methods=["POST"], endpoint=rutas["editar"])
    @login_required
    def editar(doc_id):
        escrito = None
        anterior = None
        try:
            _exigir_gestor()
            doc = db.session.query(RepositorioDocumento).filter_by(id=doc_id).first()
            if doc is None or _carpeta(ambito, doc.carpeta_id) is None:
                raise RepoError("El documento no existe.")
            doc.titulo = _titulo()
            archivo = request.files.get("archivo")
            if archivo is not None and archivo.filename:
                data, ext, original = _leer_subida(archivo)
                escrito = f"{uuid.uuid4().hex}.{ext}"
                _escribir(ambito, escrito, data)
                anterior = doc.nombre_archivo
                doc.nombre_archivo = escrito
                doc.nombre_original = original
            db.session.commit()
            flash("Documento actualizado.")
        except Exception as exc:
            if escrito:
                _borrar_archivo(ambito, escrito)
            return _fallo(ep, exc)
        if anterior and anterior != escrito:
            try:
                _borrar_archivo(ambito, anterior)
            except OSError:
                pass
        return _volver(ep)

    @app.route(f"/{slug}/borrar/<int:doc_id>", methods=["POST"], endpoint=rutas["borrar"])
    @login_required
    def borrar(doc_id):
        try:
            _exigir_gestor()
            doc = db.session.query(RepositorioDocumento).filter_by(id=doc_id).first()
            if doc is None or _carpeta(ambito, doc.carpeta_id) is None:
                raise RepoError("El documento no existe.")
            nombre = doc.nombre_archivo
            db.session.delete(doc)
            db.session.commit()
            try:
                _borrar_archivo(ambito, nombre)
            except OSError:
                pass
            flash("Documento quitado.")
            return _volver(ep)
        except Exception as exc:
            return _fallo(ep, exc)

    @app.route(f"/{slug}/archivo/<int:doc_id>", endpoint=rutas["archivo"])
    @login_required
    def archivo(doc_id):
        doc = db.session.query(RepositorioDocumento).filter_by(id=doc_id).first()
        carpeta = None
        if doc is not None:
            carpeta = db.session.query(RepositorioCarpeta).filter_by(id=doc.carpeta_id, ambito=ambito).first()
        if doc is None or carpeta is None:
            flash("El documento no existe.")
            return redirect(url_for(ep))
        try:
            ruta = _ruta_archivo(ambito, doc.nombre_archivo)
        except RepoError:
            flash("El archivo guardado no es válido.")
            return redirect(url_for(ep, anio=carpeta.anio, carpeta=carpeta.id))
        if not os.path.isfile(ruta):
            flash("No se encuentra el archivo en el servidor.")
            return redirect(url_for(ep, anio=carpeta.anio, carpeta=carpeta.id))
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
