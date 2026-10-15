"""Horario semanal: una casilla por semana del año y un PDF opcional."""
from __future__ import annotations

import logging
import os
import re
import uuid
from datetime import date, datetime

from flask import flash, redirect, render_template, request, send_file, url_for
from flask_login import current_user, login_required
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import RequestEntityTooLarge

import db
from models import HorarioSemanal

logger = logging.getLogger(__name__)

REPO_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "horario_repositorio")
os.makedirs(REPO_DIR, exist_ok=True)

_ARCHIVO_RE = re.compile(r"^[a-f0-9]{32}\.pdf$")
_MAX_BYTES = 20 * 1024 * 1024
_GESTORES = frozenset({"pserrano", "rrodriguez"})
_MESES = ("ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic")


class HorarioError(Exception):
    pass


def _usuario() -> str:
    if getattr(current_user, "is_authenticated", False):
        return (current_user.username or "").strip()
    return ""


def _puede_gestionar() -> bool:
    return _usuario().lower() in _GESTORES


def _exigir_gestor() -> None:
    if not _puede_gestionar():
        raise HorarioError("No puedes subir ni eliminar horarios.")


def _ultima_semana(anio: int) -> int:
    return date(anio, 12, 28).isocalendar().week


def _rango(lunes: date, domingo: date, anio: int) -> str:
    if lunes.month == domingo.month and lunes.year == domingo.year:
        return f"{lunes.day}–{domingo.day} {_MESES[lunes.month - 1]}"
    inicio = f"{lunes.day} {_MESES[lunes.month - 1]}"
    fin = f"{domingo.day} {_MESES[domingo.month - 1]}"
    if lunes.year != anio:
        inicio += f" {lunes.year % 100:02d}"
    if domingo.year != anio:
        fin += f" {domingo.year % 100:02d}"
    return f"{inicio}–{fin}"


def _semanas(anio: int) -> list[dict]:
    hoy = date.today()
    iso = hoy.isocalendar()
    total = _ultima_semana(anio)
    filas = []
    for numero in range(1, total + 1):
        lunes = date.fromisocalendar(anio, numero, 1)
        domingo = date.fromisocalendar(anio, numero, 7)
        filas.append({
            "numero": numero,
            "dias": _rango(lunes, domingo, anio),
            "actual": iso.year == anio and iso.week == numero,
        })
    return filas


def _anio_pedido() -> int:
    try:
        anio = int(request.args.get("anio") or request.form.get("anio") or date.today().year)
    except (TypeError, ValueError):
        anio = date.today().year
    if anio < 2000 or anio > 2100:
        raise HorarioError("El año no es válido.")
    return anio


def _semana_pedida(anio: int) -> int:
    try:
        semana = int(request.form.get("semana"))
    except (TypeError, ValueError):
        raise HorarioError("La semana no es válida.")
    if semana < 1 or semana > _ultima_semana(anio):
        raise HorarioError("Esa semana no existe en el año elegido.")
    return semana


def _anios_selector(anio: int) -> list[int]:
    hoy = date.today().year
    return list(range(min(hoy - 1, anio), max(hoy + 1, anio) + 1))


def _nombre_visible(filename: str) -> str:
    base = os.path.basename(filename or "").strip()
    base = base.encode("utf-8", "replace").decode("utf-8")
    base = "".join(ch for ch in base if ch >= " " and ch != '"' and ch != "\\").replace("/", "_")
    return (base or "horario.pdf")[:300]


def _leer_pdf(archivo) -> tuple[bytes, str]:
    if archivo is None or not getattr(archivo, "filename", ""):
        raise HorarioError("Elige un PDF.")
    visible = _nombre_visible(archivo.filename or "")
    if not visible.lower().endswith(".pdf"):
        raise HorarioError("Solo se admiten PDF.")
    try:
        archivo.seek(0)
    except Exception:
        pass
    data = archivo.read(_MAX_BYTES + 1)
    if isinstance(data, str):
        data = data.encode("latin-1", "replace")
    if not isinstance(data, (bytes, bytearray)):
        raise HorarioError("No se ha podido leer el PDF.")
    data = bytes(data)
    if not data:
        raise HorarioError("El archivo está vacío.")
    if len(data) > _MAX_BYTES:
        raise HorarioError("El archivo supera los 20 MB.")
    if b"%PDF" not in data[:1024]:
        raise HorarioError("El archivo no es un PDF.")
    return data, visible


def _ruta(nombre: str) -> str:
    if not nombre or not _ARCHIVO_RE.fullmatch(nombre):
        raise HorarioError("El archivo guardado no es válido.")
    return os.path.join(REPO_DIR, nombre)


def _escribir(nombre: str, data: bytes) -> None:
    os.makedirs(REPO_DIR, exist_ok=True)
    with open(_ruta(nombre), "wb") as salida:
        salida.write(data)


def _borrar_archivo(nombre: str) -> None:
    if not nombre:
        return
    try:
        ruta = _ruta(nombre)
    except HorarioError:
        return
    if os.path.isfile(ruta):
        os.remove(ruta)


def _volver(anio: int):
    return redirect(url_for("horario_semanal", anio=anio))


def _detalle(exc: Exception) -> str:
    texto = str(exc).strip().replace("\n", " ")
    return texto[:220]


def _fallo(exc: Exception, anio: int):
    db.session.rollback()
    logger.exception("Fallo en horario semanal")
    if isinstance(exc, HorarioError):
        flash(str(exc))
    elif isinstance(exc, RequestEntityTooLarge):
        flash("El PDF es demasiado grande. El máximo es 20 MB.")
    elif isinstance(exc, OSError):
        flash("No se ha podido guardar el PDF. La carpeta horario_repositorio no tiene permiso de escritura.")
    elif isinstance(exc, SQLAlchemyError):
        flash("No se ha podido guardar el horario en la base de datos. " + _detalle(exc))
    else:
        flash("No se ha podido completar la operación. " + _detalle(exc))
    return _volver(anio)


def register_horario_routes(app):

    @app.route("/horario-semanal")
    @login_required
    def horario_semanal():
        try:
            anio = _anio_pedido()
        except HorarioError as exc:
            flash(str(exc))
            anio = date.today().year
        semanas = _semanas(anio)
        guardados = {
            fila.semana: fila
            for fila in db.session.query(HorarioSemanal).filter_by(anio=anio).all()
        }
        for semana in semanas:
            semana["registro"] = guardados.get(semana["numero"])
        return render_template(
            "horario_semanal.html",
            anio=anio,
            anios=_anios_selector(anio),
            semanas=semanas,
            puede_gestionar=_puede_gestionar(),
        )

    @app.route("/horario-semanal/subir", methods=["POST"])
    @login_required
    def horario_semanal_subir():
        escrito = None
        anio = date.today().year
        try:
            _exigir_gestor()
            anio = _anio_pedido()
            semana = _semana_pedida(anio)
            data, original = _leer_pdf(request.files.get("archivo"))
            escrito = f"{uuid.uuid4().hex}.pdf"
            _escribir(escrito, data)
            fila = db.session.query(HorarioSemanal).filter_by(anio=anio, semana=semana).first()
            anterior = None
            if fila is None:
                fila = HorarioSemanal(anio=anio, semana=semana, fecha_subida=datetime.now())
                db.session.add(fila)
            else:
                anterior = fila.nombre_archivo
            fila.nombre_original = original
            fila.nombre_archivo = escrito
            fila.usuario = _usuario()
            fila.fecha_subida = datetime.now()
            db.session.commit()
            flash(f"Horario de la semana {semana} guardado.")
        except Exception as exc:
            if escrito:
                _borrar_archivo(escrito)
            return _fallo(exc, anio)
        if anterior and anterior != escrito:
            try:
                _borrar_archivo(anterior)
            except OSError:
                logger.exception("No se pudo borrar el PDF anterior del horario")
        return _volver(anio)

    @app.route("/horario-semanal/borrar/<int:horario_id>", methods=["POST"])
    @login_required
    def horario_semanal_borrar(horario_id):
        anio = date.today().year
        try:
            _exigir_gestor()
            anio = _anio_pedido()
            fila = db.session.query(HorarioSemanal).filter_by(id=horario_id, anio=anio).first()
            if fila is None:
                raise HorarioError("Ese horario no existe.")
            nombre = fila.nombre_archivo
            db.session.delete(fila)
            db.session.commit()
            try:
                _borrar_archivo(nombre)
            except OSError:
                logger.exception("No se pudo borrar el PDF del horario")
            flash("Horario quitado.")
            return _volver(anio)
        except Exception as exc:
            return _fallo(exc, anio)

    @app.route("/horario-semanal/archivo/<int:horario_id>")
    @login_required
    def horario_semanal_archivo(horario_id):
        fila = db.session.query(HorarioSemanal).filter_by(id=horario_id).first()
        if fila is None:
            flash("Ese horario no existe.")
            return redirect(url_for("horario_semanal"))
        try:
            ruta = _ruta(fila.nombre_archivo)
        except HorarioError:
            flash("El archivo guardado no es válido.")
            return redirect(url_for("horario_semanal", anio=fila.anio))
        if not os.path.isfile(ruta):
            flash("No se encuentra el archivo en el servidor.")
            return redirect(url_for("horario_semanal", anio=fila.anio))
        return send_file(
            ruta,
            mimetype="application/pdf",
            as_attachment=False,
            download_name=fila.nombre_original or f"semana-{fila.semana}.pdf",
            max_age=0,
            conditional=False,
        )
