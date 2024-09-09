from flask import render_template, request
import db
from datetime import datetime
from models import Transpaleta

def register_transpaletaedit_routes(app):
    #La primera función se encarga de llevar os datos al formulario de edición y la segunda es la que registra los cambios
    @app.route('/form_editar_transpaleta/<id>')
    def edicion_transpaleta(id):
        tr_editar = db.session.query(Transpaleta).filter_by(id=(id)).first()
        tr_editar_marca = tr_editar.marca
        tr_editar_modelo = tr_editar.modelo
        tr_editar_bastidor = tr_editar.bastidor
        tr_editar_asignada = tr_editar.asignada

        return render_template("form_editar_transpaleta.html", veh_editar = tr_editar,
                                                                         tr_editar_marca= tr_editar_marca,
                                                                         tr_editar_modelo= tr_editar_modelo,
                                                                         tr_editar_bastidor= tr_editar_bastidor,
                                                                         tr_editar_asignada = tr_editar_asignada)
"""    @app.route("/modificar_tacografo", methods=['POST'])
    def modificar_tacografo():
        id = request.form["id"]
        rev_tacografo=datetime.strptime(request.form["rev_tacografo_new"], "%Y-%m-%d")
        venc_tacografo=datetime.strptime(request.form["venc_tacografo_new"], "%Y-%m-%d")
        obs_tacografo=request.form["obs_tacografo_new"]
        tacografo_modificar = db.session.query(Tacografo).filter_by(id=(id)).first()
        tacografo_modificar.rev_tacografo = rev_tacografo
        tacografo_modificar.venc_tacografo = venc_tacografo
        tacografo_modificar.obs_tacografo = obs_tacografo
        db.session.commit()
        todos_tacografos = db.session.query(Tacografo).all()
        return render_template("tacografos.html", lista_tacografos=todos_tacografos)
"""