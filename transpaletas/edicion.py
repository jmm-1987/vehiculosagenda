from flask import render_template, request
import db
from datetime import datetime
from models import Transpaleta


def register_transpaletaedit_routes(app):
    # La primera función se encarga de llevar os datos al formulario de edición y la segunda es la que registra los cambios
    @app.route('/form_editar_transpaleta/<id>')
    def edicion_transpaleta(id):
        tr_editar = db.session.query(Transpaleta).filter_by(id=(id)).first()
        tr_editar_alias = tr_editar.alias
        tr_editar_marca = tr_editar.marca
        tr_editar_modelo = tr_editar.modelo
        tr_editar_bastidor = tr_editar.bastidor
        tr_editar_asignada = tr_editar.asignada

        return render_template("form_editar_transpaleta.html", tr_editar_asignada=tr_editar_asignada,
                               tr_editar_marca=tr_editar_marca,
                               tr_editar_modelo=tr_editar_modelo,
                               tr_editar_bastidor=tr_editar_bastidor,
                               tr_editar=tr_editar,
                               tr_editar_alias=tr_editar_alias)


    @app.route("/modificar_transpaleta", methods=['POST'])
    def modificar_transpaleta():
        id = request.form["id"]
        tr_modificar = db.session.query(Transpaleta).filter_by(id=(id)).first()
        tr_modificar.alias=request.form["alias_new"]
        tr_modificar.marca = request.form["marca_new"]
        tr_modificar.modelo = request.form["modelo_new"]
        tr_modificar.bastidor = request.form["bastidor_new"]
        tr_modificar.asiganar = request.form["bastidor_new"]
        db.session.commit()
        todas_transpaletas = db.session.query(Transpaleta).all()
        return render_template("transpaletas.html", lista_transpaletas=todas_transpaletas)

