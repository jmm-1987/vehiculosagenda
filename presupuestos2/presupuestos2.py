"""Tarificador de presupuestos: misma lógica que el HTML, guardada en el servidor."""
from __future__ import annotations

import json
import os
import re
import smtplib
from email.message import EmailMessage

from flask import jsonify, render_template, request
from flask_login import current_user, login_required

import db
from models import ClientePresupuesto, Presupuesto2Documento

COLECCIONES = {"clientes", "presupuestos", "ajustes", "contadores"}
_ID_RE = re.compile(r"^[A-Za-z0-9_-]{1,80}$")
_CLAVE_RE = re.compile(r"^[A-Z]{2,3}-\d{4}$")
_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
_ENV_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")


def _usuario() -> str:
    if getattr(current_user, "is_authenticated", False):
        return (current_user.username or "").strip()
    return ""


def _norm_cif(valor: str) -> str:
    return re.sub(r"[\s.-]", "", (valor or "")).upper()


def _datos(fila: Presupuesto2Documento) -> dict:
    try:
        datos = json.loads(fila.datos or "{}")
    except json.JSONDecodeError:
        datos = {}
    if not isinstance(datos, dict):
        datos = {}
    datos["id"] = fila.doc_id
    return datos


def _guardar(coleccion: str, doc_id: str, datos: dict) -> None:
    limpio = {k: v for k, v in datos.items() if k != "id"}
    fila = (
        db.session.query(Presupuesto2Documento)
        .filter_by(coleccion=coleccion, doc_id=doc_id)
        .first()
    )
    texto = json.dumps(limpio, ensure_ascii=False)
    if fila is None:
        db.session.add(Presupuesto2Documento(coleccion=coleccion, doc_id=doc_id, datos=texto))
    else:
        fila.datos = texto


def _marca_importacion() -> bool:
    fila = (
        db.session.query(Presupuesto2Documento)
        .filter_by(coleccion="ajustes", doc_id="importacion_clientes")
        .first()
    )
    if fila is None:
        return False
    return bool(_datos(fila).get("hecha"))


def _importar_clientes_actuales() -> None:
    if _marca_importacion():
        return
    existentes = db.session.query(Presupuesto2Documento).filter_by(coleccion="clientes").all()
    cifs = {_norm_cif(_datos(fila).get("cif", "")) for fila in existentes}
    for cliente in db.session.query(ClientePresupuesto).order_by(ClientePresupuesto.id).all():
        cif = _norm_cif(cliente.cif)
        if cif and cif in cifs:
            continue
        doc_id = f"imp-{cliente.id}"
        if any(fila.doc_id == doc_id for fila in existentes):
            continue
        _guardar("clientes", doc_id, {
            "nombre": cliente.nombre or "",
            "cif": cliente.cif or "",
            "dir": cliente.direccion or "",
            "cp": "",
            "pob": cliente.poblacion or "",
            "prov": "",
            "pais": "ES",
            "tel": cliente.telefono or "",
            "email": cliente.email or "",
            "importado": True,
        })
        if cif:
            cifs.add(cif)
    _guardar("ajustes", "importacion_clientes", {"hecha": True})
    db.session.commit()


def _leer_env() -> dict:
    valores = {}
    if os.path.isfile(_ENV_PATH):
        with open(_ENV_PATH, encoding="utf-8") as archivo:
            for linea in archivo:
                linea = linea.strip()
                if not linea or linea.startswith("#") or "=" not in linea:
                    continue
                clave, valor = linea.split("=", 1)
                valores[clave.strip()] = valor.strip().strip('"').strip("'")
    return valores


def _cfg(valores: dict, clave: str, defecto: str = "") -> str:
    if valores.get(clave):
        return valores[clave]
    return os.environ.get(clave, defecto)


def _contacto_presupuesto(codigo: str, serie: str) -> str:
    serie = (serie or "").strip().upper()
    codigo = (codigo or "").strip().upper()
    if serie == "NAV" or codigo.startswith("NAV"):
        return "presupuestosnavalmoral@alditraex.es"
    return "presupuestos@alditraex.es"


def _email_de_quien_envia() -> str:
    if not getattr(current_user, "is_authenticated", False):
        return ""
    email = (getattr(current_user, "email", None) or "").strip().lower()
    if _EMAIL_RE.fullmatch(email):
        return email
    return ""


def _enviar_pdf(destino: str, codigo: str, pdf: bytes, nombre: str, serie: str = "", copia: str = "") -> str | None:
    valores = _leer_env()
    host = _cfg(valores, "SMTP_HOST")
    usuario = _cfg(valores, "SMTP_USER")
    password = _cfg(valores, "SMTP_PASSWORD")
    remitente = _cfg(valores, "SMTP_FROM") or usuario
    if not host or not usuario or not password or not remitente:
        return "La cuenta de envío no está configurada. Rellena el archivo .env y reinicia la aplicación."
    try:
        puerto = int(_cfg(valores, "SMTP_PORT", "587") or "587")
    except ValueError:
        return "SMTP_PORT no es un número."
    tls = _cfg(valores, "SMTP_USE_TLS", "1").lower() not in ("0", "false", "no")
    mensaje = EmailMessage()
    mensaje["Subject"] = f"Presupuesto {codigo}" if codigo else "Presupuesto Alditraex"
    mensaje["From"] = remitente
    mensaje["To"] = destino
    if copia and copia != destino:
        mensaje["Cc"] = copia
    ref = f" {codigo}" if codigo else ""
    contacto = _contacto_presupuesto(codigo, serie)
    mensaje.set_content(
        f"Adjuntamos el presupuesto solicitado{ref}\n\n"
        "Quedamos pendientes de recibir el justificante de ingreso para poder poner en marcha el servicio solicitado\n\n"
        f"Si tiene alguna duda contacte con {contacto}\n\n"
        "Muchas gracias"
    )
    mensaje.add_attachment(pdf, maintype="application", subtype="pdf", filename=nombre or "presupuesto.pdf")
    try:
        with smtplib.SMTP(host, puerto, timeout=30) as smtp:
            if tls:
                smtp.starttls()
            smtp.login(usuario, password)
            smtp.send_message(mensaje)
    except Exception:
        return "No se pudo enviar el email. Revisa los datos de la cuenta en el archivo .env."
    return None


def register_presupuestos2_routes(app):
    @app.route("/presupuestos2")
    @login_required
    def presupuestos2():
        _importar_clientes_actuales()
        return render_template("presupuestos2.html", usuario=_usuario())

    @app.route("/api/presupuestos2/<coleccion>")
    @login_required
    def presupuestos2_lista(coleccion):
        if coleccion not in COLECCIONES:
            return jsonify({"ok": False, "error": "Colección no válida"}), 404
        if coleccion == "clientes":
            _importar_clientes_actuales()
        filas = (
            db.session.query(Presupuesto2Documento)
            .filter_by(coleccion=coleccion)
            .all()
        )
        return jsonify([_datos(fila) for fila in filas])

    @app.route("/api/presupuestos2/<coleccion>/<doc_id>", methods=["PUT"])
    @login_required
    def presupuestos2_guardar(coleccion, doc_id):
        if coleccion not in COLECCIONES or not _ID_RE.fullmatch(doc_id):
            return jsonify({"ok": False, "error": "Identificador no válido"}), 400
        datos = request.get_json(silent=True)
        if not isinstance(datos, dict):
            return jsonify({"ok": False, "error": "Datos no válidos"}), 400
        _guardar(coleccion, doc_id, datos)
        db.session.commit()
        return jsonify({"ok": True})

    @app.route("/api/presupuestos2/<coleccion>/<doc_id>", methods=["DELETE"])
    @login_required
    def presupuestos2_borrar(coleccion, doc_id):
        if coleccion not in COLECCIONES or not _ID_RE.fullmatch(doc_id):
            return jsonify({"ok": False, "error": "Identificador no válido"}), 400
        fila = (
            db.session.query(Presupuesto2Documento)
            .filter_by(coleccion=coleccion, doc_id=doc_id)
            .first()
        )
        if fila is not None:
            db.session.delete(fila)
            db.session.commit()
        return jsonify({"ok": True})

    @app.route("/api/presupuestos2/siguiente-numero", methods=["POST"])
    @login_required
    def presupuestos2_siguiente_numero():
        datos = request.get_json(silent=True) or {}
        clave = datos.get("key") or ""
        if not _CLAVE_RE.fullmatch(clave):
            return jsonify({"ok": False, "error": "Clave no válida"}), 400
        usados = []
        for valor in datos.get("usados") or []:
            try:
                usados.append(int(valor))
            except (TypeError, ValueError):
                continue
        fila = (
            db.session.query(Presupuesto2Documento)
            .filter_by(coleccion="contadores", doc_id=clave)
            .first()
        )
        actual = 0
        if fila is not None:
            try:
                actual = int(_datos(fila).get("ultimo") or 0)
            except (TypeError, ValueError):
                actual = 0
        numero = max([actual, *usados, 0]) + 1
        _guardar("contadores", clave, {"ultimo": numero})
        db.session.commit()
        return jsonify({"ok": True, "numero": numero})

    @app.route("/api/presupuestos2/enviar", methods=["POST"])
    @login_required
    def presupuestos2_enviar():
        destino = (request.form.get("email") or "").strip().lower()
        if not _EMAIL_RE.fullmatch(destino):
            return jsonify({"ok": False, "error": "El email de envío no es válido."}), 400
        archivo = request.files.get("archivo")
        if archivo is None or not archivo.filename:
            return jsonify({"ok": False, "error": "No llega el PDF."}), 400
        pdf = archivo.read(15 * 1024 * 1024 + 1)
        if not pdf:
            return jsonify({"ok": False, "error": "El PDF está vacío."}), 400
        if len(pdf) > 15 * 1024 * 1024:
            return jsonify({"ok": False, "error": "El PDF supera los 15 MB."}), 400
        codigo = (request.form.get("codigo") or "").strip()[:40]
        serie = (request.form.get("serie") or "").strip()[:12]
        nombre = os.path.basename(archivo.filename).replace('"', "")[:120] or "presupuesto.pdf"
        copia = _email_de_quien_envia()
        error = _enviar_pdf(destino, codigo, pdf, nombre, serie, copia)
        if error:
            return jsonify({"ok": False, "error": error})
        if not copia:
            return jsonify({
                "ok": True,
                "aviso": "Presupuesto enviado. Este usuario no tiene email en el manager, así que no se le ha mandado copia.",
            })
        return jsonify({"ok": True, "copia": copia})
