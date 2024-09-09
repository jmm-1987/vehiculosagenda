from flask import render_template, request
import db
from datetime import datetime
from models import Itv

def register_itvedit_routes(app):
    @app.route('/form_editar_itv/<id>')
    def edicion_itv(id):
        veh_editar = db.session.query(Itv).filter_by(id=(id)).first()
        veh_editar_fecha_itv = veh_editar.fecha_itv
        veh_editar_venc_itv = veh_editar.venc_itv
        veh_editar_cita_itv = veh_editar.cita_itv

        return render_template("form_editar_itv.html", veh_editar = veh_editar,
                                                                         veh_editar_fecha_itv= veh_editar_fecha_itv,
                                                                         veh_editar_venc_itv= veh_editar_venc_itv,
                                                                         veh_editar_cita_itv= veh_editar_cita_itv)

    @app.route("/modificar_itv", methods=['POST'])
    def modificar_itv():
        id = request.form["id"]
        fecha_itv=datetime.strptime(request.form["fecha_itv_new"], "%Y-%m-%d")
        vencimiento_itv=datetime.strptime(request.form["vencimiento_itv_new"], "%Y-%m-%d")
        cita_itv=datetime.strptime(request.form["cita_itv_new"], "%Y-%m-%d")
        obs_itv = request.form["observaciones_itv_new"]
        itv_modificar = db.session.query(Itv).filter_by(id=(id)).first()
        itv_modificar.fecha_itv = fecha_itv
        itv_modificar.venc_itv = vencimiento_itv
        itv_modificar.cita_itv = cita_itv
        itv_modificar.obs_itv = obs_itv
        db.session.commit()
        todas_itv = db.session.query(Itv).all()
        return render_template("itv.html", lista_itv=todas_itv)
