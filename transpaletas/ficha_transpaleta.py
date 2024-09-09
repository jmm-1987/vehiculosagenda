from flask import render_template
import db
from models import Transpaleta, Visita

def register_transpaleta_talleres_routes(app):
    @app.route("/talleres_transpaleta/<id>")
    def talleres_transpaleta(id):
        t_ficha_alias = db.session.query(Transpaleta.alias).filter_by(id=(id)).scalar()
        t_ficha_id = db.session.query(Transpaleta.id).filter_by(id=(id)).scalar()
        t_ficha = db.session.query(Visita).filter_by(alias=(t_ficha_alias)).all()


        return render_template("talleres_transpaleta.html", t_ficha_alias=t_ficha_alias,
                                                                              t_ficha=t_ficha,
                                                                              t_ficha_id=t_ficha_id)
