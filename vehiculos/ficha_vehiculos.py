from flask import render_template
import db
from models import Vehiculo, Itv, Seguro,Tacografo,Rodaje,Extintor

def register_ficha_routes(app):
    @app.route("/ficha/<id>")
    def ficha(id):
        veh_ficha_mat = db.session.query(Vehiculo.matricula).filter_by(id=(id)).scalar()
        veh_ficha_alias = db.session.query(Vehiculo.alias).filter_by(id=(id)).scalar()
        veh_ficha_ficha = db.session.query(Vehiculo.doc_ficha).filter_by(id=(id)).scalar()
        veh_ficha_permiso = db.session.query(Vehiculo.doc_permiso).filter_by(id=(id)).scalar()
        itv_ficha = db.session.query(Itv).filter_by(matricula=(veh_ficha_mat))
        seguro_ficha = db.session.query(Seguro).filter_by(matricula=(veh_ficha_mat))
        tacografo_ficha = db.session.query(Tacografo).filter_by(matricula=(veh_ficha_mat))
        rodaje_ficha = db.session.query(Rodaje).filter_by(matricula=(veh_ficha_mat))
        extintor_ficha = db.session.query(Extintor).filter_by(matricula=(veh_ficha_mat))

        return render_template("ficha.html", veh_ficha_mat=veh_ficha_mat,
                                                               veh_ficha_alias=veh_ficha_alias,
                                                               itv_ficha =itv_ficha,
                                                               seguro_ficha= seguro_ficha,
                                                               tacografo_ficha = tacografo_ficha,
                                                               rodaje_ficha = rodaje_ficha,
                                                               extintor_ficha = extintor_ficha,
                                                               veh_ficha_ficha=veh_ficha_ficha,
                                                               veh_ficha_permiso=veh_ficha_permiso,
                                                               id=id)
