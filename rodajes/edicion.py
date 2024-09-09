from flask import render_template, request
import db
from datetime import datetime
from models import Rodaje

def register_rodajeedit_routes(app):
    @app.route('/form_editar_rodaje/<id>')
    def edicion_rodaje(id):
        veh_editar = db.session.query(Rodaje).filter_by(id=(id)).first()
        veh_editar_pago_rodaje = veh_editar.pago_rodaje
        veh_editar_venc_rodaje = veh_editar.venc_rodaje
        veh_editar_obs_rodaje = veh_editar.obs_rodaje
        veh_editar_imp_rodaje = veh_editar.imp_rodaje

        return render_template("form_editar_rodaje.html", veh_editar = veh_editar,
                                                                         veh_editar_pago_rodaje= veh_editar_pago_rodaje,
                                                                         veh_editar_venc_rodaje= veh_editar_venc_rodaje,
                                                                         veh_editar_obs_rodaje= veh_editar_obs_rodaje,
                                                                         veh_editar_imp_rodaje=veh_editar_imp_rodaje)

    @app.route("/modificar_rodaje", methods=['POST'])
    def modificar_rodaje():
        id = request.form["id"]
        pago_rodaje=datetime.strptime(request.form["fecha_pago_new"], "%Y-%m-%d")
        venc_rodaje=datetime.strptime(request.form["venc_rodaje_new"], "%Y-%m-%d")
        obs_rodaje = request.form["obs_rodaje_new"]
        imp_rodaje=request.form["imp_rodaje_new"]
        rodaje_modificar = db.session.query(Rodaje).filter_by(id=(id)).first()
        rodaje_modificar.pago_rodaje = pago_rodaje
        rodaje_modificar.venc_rodaje = venc_rodaje
        rodaje_modificar.obs_rodaje = obs_rodaje
        rodaje_modificar.imp_rodaje = imp_rodaje
        db.session.commit()
        todos_rodajes = db.session.query(Rodaje).all()
        return render_template("rodajes.html", lista_rodajes=todos_rodajes)
