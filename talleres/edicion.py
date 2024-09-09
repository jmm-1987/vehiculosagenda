from flask import render_template, request
import db
from datetime import datetime
from models import Taller, Vehiculo

def register_talleredit_routes(app):
    #La primera función se encarga de llevar os datos al formulario de edición y la segunda es la que registra los cambios
    @app.route('/form_editar_taller/<id>')
    def edicion_taller(id):
        taller_editar = db.session.query(Taller).filter_by(id=(id)).first()

        return render_template("form_editar_taller.html", taller_editar = taller_editar)

    @app.route("/modificar_taller", methods=["POST", "GET"])
    def modificar_taller():
        id = request.form["id"]
        taller=request.form["taller_new"]
        fecha_visita = datetime.strptime(request.form["fecha_visita_new"],"%Y-%m-%d")
        kilometros = request.form["kilometros_new"]
        problema = request.form["problema_new"]
        albaran = request.form["albaran_new"]
        presupuesto = request.form["presupuesto_new"]
        trabajos = request.form["trabajos_new"]
        importe = request.form["importe_new"]
        fecha_entrega_str = request.form.get("fecha_entrega_new")
        if fecha_entrega_str:
            fecha_entrega = datetime.strptime(request.form["fecha_entrega_new"], "%Y-%m-%d")
            activo = False
        else:
            fecha_entrega = None
            activo = True
        taller_modificar = db.session.query(Taller).filter_by(id=(id)).first()
        taller_modificar.kilometros = kilometros
        taller_modificar.taller = taller
        taller_modificar.fecha_visita = fecha_visita
        taller_modificar.problema = problema
        taller_modificar.albaran = albaran
        taller_modificar.presupuesto = presupuesto
        taller_modificar.trabajos = trabajos
        taller_modificar.importe = importe
        taller_modificar.fecha_entrega = fecha_entrega
        taller_modificar.activo = activo
        db.session.commit()
        matriculas = db.session.query(Vehiculo.matricula).filter(Vehiculo.activo == True).all()

        todos_talleres = db.session.query(Taller).order_by(Taller.fecha_visita.desc()).all()
        return render_template("talleres.html", lista_talleres=todos_talleres, lista_matriculas=matriculas)
