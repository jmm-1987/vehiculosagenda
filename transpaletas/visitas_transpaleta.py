from flask import render_template, redirect, url_for, request
from flask_login import login_required
import db
from datetime import datetime
from models import Transpaleta, Visita


def register_visitas_transapaleta_routes(app):
    @app.route('/formulario_visita_transpaleta/<id>')
    def formulario_visita_transpaleta(id):
        transpaleta = db.session.query(Transpaleta).filter_by(id=(id)).first()
        return render_template("crear_visita_transpaleta.html", transpaleta=transpaleta)

    @app.route("/crear_visita_transpaleta", methods=["POST", "GET"])
    def crear_visita_transpaleta():
        fecha_entrega_str = request.form.get("fecha_entrega")
        if fecha_entrega_str:
            fecha_entrega = datetime.strptime(fecha_entrega_str, '%Y-%m-%d')
            finalizado = False
        else:
            fecha_entrega = None
            finalizado = True
        visita = Visita(alias=request.form["alias"],
                        taller=request.form["taller"],
                        problema =request.form["problema"],
                        albaran=request.form["albaran"],
                        presupuesto=request.form["presupuesto"],
                        fecha_visita=datetime.strptime(request.form["fecha_visita"], '%Y-%m-%d'),
                        trabajos=request.form["trabajos"],
                        importe =request.form["importe"],
                        fecha_entrega=fecha_entrega,
                        finalizado=finalizado)

        db.session.add(visita)
        db.session.commit()
        return redirect(url_for('lista_transpaletas'))

    @app.route('/ver_visita/<id>')
    def ver_visita(id):
        visita_ver = db.session.query(Visita).filter_by(id=(id)).first()
        return render_template("ver_visita.html", visita_ver=visita_ver)

    @app.route("/form_editar_visita/<id>")
    def edicion_visita(id):
        visita_editar = db.session.query(Visita).filter_by(id=(id)).first()

        return render_template("form_editar_visita.html", visita_editar=visita_editar)

    @app.route("/modificar_visita", methods=["POST", "GET"])
    def modificar_visita():
        id = request.form["id"]
        taller = request.form["taller_new"]
        fecha_visita = datetime.strptime(request.form["fecha_visita_new"], "%Y-%m-%d")
        problema = request.form["problema_new"]
        albaran = request.form["albaran_new"]
        presupuesto = request.form["presupuesto_new"]
        trabajos = request.form["trabajos_new"]
        importe = request.form["importe_new"]
        fecha_entrega_str = request.form.get("fecha_entrega_new")
        if fecha_entrega_str:
            fecha_entrega = datetime.strptime(request.form["fecha_entrega_new"], "%Y-%m-%d")
            finalizado = False
        else:
            fecha_entrega = None
            finalizado = True
        visita_modificar = db.session.query(Visita).filter_by(id=(id)).first()
        visita_modificar.taller = taller
        visita_modificar.fecha_visita = fecha_visita
        visita_modificar.problema = problema
        visita_modificar.albaran = albaran
        visita_modificar.presupuesto = presupuesto
        visita_modificar.trabajos = trabajos
        visita_modificar.importe = importe
        visita_modificar.fecha_entrega = fecha_entrega
        visita_modificar.finalizado = finalizado
        db.session.commit()
        todos_talleres = db.session.query(Visita).all()
        print(id)
        return redirect(url_for("talleres_transpaleta", id=id, lista_talleres=todos_talleres))

    @app.route("/borrar_visita/<id>", methods=["POST", "GET"])
    def borrar_visita(id):
        registro_borrar = db.session.query(Visita).filter_by(id=id).first()
        db.session.delete(registro_borrar)
        db.session.commit()
        return redirect(url_for('lista_transpaletas'))

    #"/talleres_transpaleta/{{visita_editar.id}}"   url_for('edicion_visita', id=t.id)
    #redirect(url_for("buscador_tickets_selector", id=registro_para_url))


