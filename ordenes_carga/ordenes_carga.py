import os
import re
from datetime import datetime, date

from flask import render_template, redirect, url_for, request, jsonify, send_file, flash, current_app
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename

import db
from models import OrdenCargaInternacional, ClienteOrdenCarga
from ordenes_carga.generar_pdf_orden import combinar_pdf_orden

ORDEN_CARGA_START_NUM = 160
UPLOAD_SUBDIR = "ordenes_carga"


def _upload_dir():
    path = os.path.join(current_app.root_path, "static", "subidas", UPLOAD_SUBDIR)
    os.makedirs(path, exist_ok=True)
    return path


def _sufijo_anio():
    return datetime.now().strftime("%y")


def _parse_fecha(val):
    if not val:
        return None
    try:
        return datetime.strptime(val, "%Y-%m-%d").date()
    except ValueError:
        return None


def _parse_importe(val):
    if val is None or val == "":
        return 0.0
    s = str(val).replace(".", "").replace(",", ".")
    s = re.sub(r"[^0-9.\-]", "", s)
    try:
        return float(s)
    except ValueError:
        return 0.0


def _format_importe(n):
    if n is None:
        return "0,00"
    return f"{n:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def obtener_siguiente_numero_orden():
    sufijo = _sufijo_anio()
    patron = re.compile(rf"^(\d+)/{sufijo}$")
    max_num = ORDEN_CARGA_START_NUM - 1
    filas = db.session.query(OrdenCargaInternacional.numero_orden).all()
    for (numero,) in filas:
        if not numero:
            continue
        m = patron.match(numero.strip())
        if m:
            n = int(m.group(1))
            if n > max_num:
                max_num = n
    return f"{max_num + 1}/{sufijo}"


def _guardar_cliente_entrega(datos):
    nombre = (datos.get("nombre_entrega") or "").strip()
    if not nombre:
        return
    cliente = db.session.query(ClienteOrdenCarga).filter_by(nombre=nombre).first()
    if not cliente:
        cliente = ClienteOrdenCarga(nombre=nombre)
        db.session.add(cliente)
    cliente.direccion = datos.get("direccion", "") or ""
    cliente.cp = datos.get("cp", "") or ""
    cliente.poblacion = datos.get("poblacion", "") or ""
    cliente.pais = datos.get("pais", "") or ""
    cliente.telefono = datos.get("telefono", "") or ""
    cliente.contacto = datos.get("contacto", "") or ""
    cliente.activo = True


def _orden_desde_form(form, orden=None):
    if orden is None:
        orden = OrdenCargaInternacional(
            numero_orden=form.get("numero_orden", "").strip(),
            fecha_emision=_parse_fecha(form.get("fecha_emision")) or date.today(),
            fecha_creacion=datetime.now(),
            usuario_creacion=current_user.username if current_user else "",
        )
    orden.numero_orden = form.get("numero_orden", orden.numero_orden).strip()
    orden.fecha_emision = _parse_fecha(form.get("fecha_emision")) or orden.fecha_emision
    orden.fecha_carga = _parse_fecha(form.get("fecha_carga"))
    orden.fecha_prevista_llegada = _parse_fecha(form.get("fecha_prevista_llegada"))
    orden.proveedor = form.get("proveedor", "") or ""
    orden.referencia = form.get("referencia", "") or ""
    orden.pallets = form.get("pallets", "") or ""
    orden.peso_kg = form.get("peso_kg", "") or ""
    orden.volumen_m3 = form.get("volumen_m3", "") or ""
    orden.nombre_entrega = form.get("nombre_entrega", "") or ""
    orden.direccion = form.get("direccion", "") or ""
    orden.cp = form.get("cp", "") or ""
    orden.poblacion = form.get("poblacion", "") or ""
    orden.pais = form.get("pais", "") or ""
    orden.telefono = form.get("telefono", "") or ""
    orden.contacto = form.get("contacto", "") or ""
    orden.observaciones = form.get("observaciones", "") or ""
    orden.portes = _parse_importe(form.get("portes"))
    orden.maut_lsva = _parse_importe(form.get("maut_lsva"))
    orden.carburante = _parse_importe(form.get("carburante"))
    orden.total = orden.portes + orden.maut_lsva + orden.carburante
    return orden


def _adjunto_path(orden):
    if not orden or not orden.pdf_adjunto:
        return None
    path = os.path.join(_upload_dir(), orden.pdf_adjunto)
    return path if os.path.isfile(path) else None


def register_ordenes_carga_routes(app):

    @app.route("/ordenes_carga_internacionales")
    @login_required
    def lista_ordenes_carga():
        ordenes = db.session.query(OrdenCargaInternacional).filter(
            OrdenCargaInternacional.activo == True
        ).order_by(OrdenCargaInternacional.id.desc()).all()
        return render_template("ordenes_carga_lista.html", ordenes=ordenes)

    @app.route("/ordenes_carga_internacionales/nueva")
    @login_required
    def nueva_orden_carga():
        orden = OrdenCargaInternacional(
            numero_orden=obtener_siguiente_numero_orden(),
            fecha_emision=date.today(),
            fecha_creacion=datetime.now(),
        )
        clientes = db.session.query(ClienteOrdenCarga).filter(
            ClienteOrdenCarga.activo == True
        ).order_by(ClienteOrdenCarga.nombre).all()
        return render_template(
            "orden_carga_form.html",
            orden=orden,
            clientes=clientes,
            es_nueva=True,
            format_importe=_format_importe,
        )

    @app.route("/ordenes_carga_internacionales/<int:id>/editar")
    @login_required
    def editar_orden_carga(id):
        orden = db.session.query(OrdenCargaInternacional).filter_by(id=id).first()
        if not orden:
            return redirect(url_for("lista_ordenes_carga"))
        clientes = db.session.query(ClienteOrdenCarga).filter(
            ClienteOrdenCarga.activo == True
        ).order_by(ClienteOrdenCarga.nombre).all()
        return render_template(
            "orden_carga_form.html",
            orden=orden,
            clientes=clientes,
            es_nueva=False,
            format_importe=_format_importe,
        )

    @app.route("/ordenes_carga_internacionales/guardar", methods=["POST"])
    @login_required
    def guardar_orden_carga():
        orden_id = request.form.get("id", "").strip()
        try:
            if orden_id:
                orden = db.session.query(OrdenCargaInternacional).filter_by(id=int(orden_id)).first()
                if not orden:
                    flash("Orden no encontrada", "error")
                    return redirect(url_for("lista_ordenes_carga"))
            else:
                orden = None
            orden = _orden_desde_form(request.form, orden)
            if not orden.numero_orden:
                flash("El número de orden es obligatorio", "error")
                return redirect(url_for("nueva_orden_carga"))

            archivo = request.files.get("pdf_adjunto")
            if archivo and archivo.filename:
                nombre = secure_filename(archivo.filename)
                if not nombre.lower().endswith(".pdf"):
                    flash("El adjunto debe ser un archivo PDF", "error")
                    return redirect(request.referrer or url_for("lista_ordenes_carga"))
                if orden.id:
                    fname = f"orden_{orden.id}_{nombre}"
                else:
                    fname = f"orden_tmp_{datetime.now().strftime('%Y%m%d%H%M%S')}_{nombre}"
                archivo.save(os.path.join(_upload_dir(), fname))
                if orden.pdf_adjunto and orden.pdf_adjunto != fname:
                    old = os.path.join(_upload_dir(), orden.pdf_adjunto)
                    if os.path.isfile(old):
                        try:
                            os.remove(old)
                        except OSError:
                            pass
                orden.pdf_adjunto = fname

            if not orden_id:
                db.session.add(orden)
                db.session.flush()
                if orden.pdf_adjunto and orden.pdf_adjunto.startswith("orden_tmp_"):
                    nuevo = f"orden_{orden.id}_{orden.pdf_adjunto.split('_', 3)[-1]}"
                    os.rename(
                        os.path.join(_upload_dir(), orden.pdf_adjunto),
                        os.path.join(_upload_dir(), nuevo),
                    )
                    orden.pdf_adjunto = nuevo

            _guardar_cliente_entrega({
                "nombre_entrega": orden.nombre_entrega,
                "direccion": orden.direccion,
                "cp": orden.cp,
                "poblacion": orden.poblacion,
                "pais": orden.pais,
                "telefono": orden.telefono,
                "contacto": orden.contacto,
            })
            db.session.commit()
            flash("Orden guardada correctamente", "success")
            return redirect(url_for("editar_orden_carga", id=orden.id))
        except IntegrityError:
            db.session.rollback()
            flash("Ya existe una orden con ese número", "error")
            return redirect(request.referrer or url_for("lista_ordenes_carga"))
        except Exception as e:
            db.session.rollback()
            flash(f"Error al guardar: {e}", "error")
            return redirect(request.referrer or url_for("lista_ordenes_carga"))

    @app.route("/ordenes_carga_internacionales/<int:id>/borrar", methods=["POST"])
    @login_required
    def borrar_orden_carga(id):
        orden = db.session.query(OrdenCargaInternacional).filter_by(id=id).first()
        if orden:
            orden.activo = False
            db.session.commit()
        return redirect(url_for("lista_ordenes_carga"))

    @app.route("/ordenes_carga_internacionales/<int:id>/eliminar-adjunto", methods=["POST"])
    @login_required
    def eliminar_adjunto_orden(id):
        orden = db.session.query(OrdenCargaInternacional).filter_by(id=id).first()
        if orden and orden.pdf_adjunto:
            path = os.path.join(_upload_dir(), orden.pdf_adjunto)
            if os.path.isfile(path):
                try:
                    os.remove(path)
                except OSError:
                    pass
            orden.pdf_adjunto = ""
            db.session.commit()
        return redirect(url_for("editar_orden_carga", id=id))

    @app.route("/ordenes_carga_internacionales/<int:id>/imprimir")
    @login_required
    def imprimir_orden_carga(id):
        orden = db.session.query(OrdenCargaInternacional).filter_by(id=id).first()
        if not orden:
            return redirect(url_for("lista_ordenes_carga"))
        return render_template(
            "orden_carga_imprimir.html",
            orden=orden,
            format_importe=_format_importe,
            tiene_adjunto=bool(_adjunto_path(orden)),
        )

    @app.route("/ordenes_carga_internacionales/<int:id>/pdf-combinado")
    @login_required
    def pdf_combinado_orden_carga(id):
        orden = db.session.query(OrdenCargaInternacional).filter_by(id=id).first()
        if not orden:
            return "Orden no encontrada", 404
        html = render_template(
            "orden_carga_imprimir.html",
            orden=orden,
            format_importe=_format_importe,
            tiene_adjunto=False,
            solo_pdf=True,
        )
        try:
            static_dir = os.path.join(current_app.root_path, "static")
            pdf_bytes = combinar_pdf_orden(html, _adjunto_path(orden), archive=static_dir)
        except Exception as e:
            return f"Error generando PDF: {e}", 500
        return send_file(
            __import__("io").BytesIO(pdf_bytes),
            mimetype="application/pdf",
            as_attachment=False,
            download_name=f"orden_carga_{orden.numero_orden.replace('/', '-')}.pdf",
        )

    @app.route("/api/ordenes_carga/siguiente_numero")
    @login_required
    def api_siguiente_numero_orden():
        return jsonify({"numero": obtener_siguiente_numero_orden()})

    @app.route("/api/ordenes_carga/clientes")
    @login_required
    def api_clientes_orden_carga():
        clientes = db.session.query(ClienteOrdenCarga).filter(
            ClienteOrdenCarga.activo == True
        ).order_by(ClienteOrdenCarga.nombre).all()
        return jsonify({
            c.nombre: {
                "direccion": c.direccion or "",
                "cp": c.cp or "",
                "poblacion": c.poblacion or "",
                "pais": c.pais or "",
                "telefono": c.telefono or "",
                "contacto": c.contacto or "",
            }
            for c in clientes
        })
