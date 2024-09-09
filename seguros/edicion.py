from flask import render_template, request
import db
from datetime import datetime
from models import Seguro

def register_seguroedit_routes(app):
    #La primera función se encarga de llevar os datos al formulario de edición y la segunda es la que registra los cambios
    @app.route('/form_editar_seguro/<id>')
    def edicion_seguro(id):
        veh_editar = db.session.query(Seguro).filter_by(id=(id)).first()
        veh_editar_venc_seguro = veh_editar.venc_seguro
        veh_editar_cia_seguro = veh_editar.cia_seguro
        veh_editar_cob_seguro = veh_editar.cob_seguro
        veh_editar_fra_seguro = veh_editar.fra_seguro
        veh_editar_pri_seguro = veh_editar.pri_seguro
        veh_editar_obs_seguro = veh_editar.obs_seguro

        return render_template("form_editar_seguro.html", veh_editar = veh_editar,
                                                                         veh_editar_venc_seguro= veh_editar_venc_seguro,
                                                                         veh_editar_cia_seguro= veh_editar_cia_seguro,
                                                                         veh_editar_cob_seguro= veh_editar_cob_seguro,
                                                                         veh_editar_fra_seguro=veh_editar_fra_seguro,
                                                                         veh_editar_pri_seguro=veh_editar_pri_seguro,
                                                                         veh_editar_obs_seguro=veh_editar_obs_seguro )

    @app.route("/modificar_seguro", methods=['POST'])
    def modificar_seguro():
        id = request.form["id"]
        venc_seguro=datetime.strptime(request.form["venc_seguro_new"], "%Y-%m-%d")
        cia_seguro=request.form["cia_seguro_new"]
        cob_seguro=request.form["cob_seguro_new"]
        fra_seguro = request.form["fra_seguro_new"]
        pri_seguro = request.form["pri_seguro_new"]
        obs_seguro = request.form["obs_seguro_new"]
        seguro_modificar = db.session.query(Seguro).filter_by(id=(id)).first()
        seguro_modificar.venc_seguro = venc_seguro
        seguro_modificar.cia_seguro = cia_seguro
        seguro_modificar.cob_seguro = cob_seguro
        seguro_modificar.fra_seguro = fra_seguro
        seguro_modificar.pri_seguro = pri_seguro
        seguro_modificar.obs_seguro = obs_seguro
        db.session.commit()
        todos_seguros = db.session.query(Seguro).all()
        return render_template("seguros.html", lista_seguros=todos_seguros)
