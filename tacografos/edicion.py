from flask import render_template, request
import db
from datetime import datetime
from models import Tacografo

def register_tacografoedit_routes(app):
    #La primera función se encarga de llevar os datos al formulario de edición y la segunda es la que registra los cambios
    @app.route('/form_editar_tacografo/<id>')
    def edicion_tacografo(id):
        veh_editar = db.session.query(Tacografo).filter_by(id=(id)).first()
        veh_editar_rev_tacografo = veh_editar.rev_tacografo
        veh_editar_venc_tacografo = veh_editar.venc_tacografo
        veh_editar_obs_tacografo = veh_editar.obs_tacografo

        return render_template("form_editar_tacografo.html", veh_editar = veh_editar,
                                                                         veh_editar_rev_tacografo= veh_editar_rev_tacografo,
                                                                         veh_editar_venc_tacografo= veh_editar_venc_tacografo,
                                                                         veh_editar_obs_tacografo= veh_editar_obs_tacografo)
    @app.route("/modificar_tacografo", methods=['POST'])
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
