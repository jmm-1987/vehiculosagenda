from flask import render_template, redirect, url_for, request
from flask_login import login_required
import db
from datetime import datetime
from models import Rodaje, Vehiculo


def register_rodajes_routes(app):
    @app.route('/rodajes')
    @login_required
    def lista_rodajes():
        todos_rodajes = db.session.query(Rodaje).filter(Rodaje.activo == True).all()
        return render_template('rodajes.html', lista_rodajes=todos_rodajes)

    @app.route('/rodajes_todos')
    def lista_rodajes_todos():
        todos_rodajes = db.session.query(Rodaje).all()
        return render_template('rodajes.html', lista_rodajes=todos_rodajes)

    @app.route('/formulario_rodaje')
    def formulario_rodaje():
        matriculas = db.session.query(Vehiculo.matricula).all()
        return render_template("crear_rodaje.html", lista_matriculas=matriculas)

    @app.route("/borrar_rodaje/<id>", methods=["POST", "GET"])
    def borrar_rodaje(id):
        registro_borrar = db.session.query(Rodaje).filter_by(id=id).first()
        db.session.delete(registro_borrar)
        db.session.commit()
        return redirect(url_for('lista_rodajes'))

    @app.route("/crear_rodaje", methods=["POST", "GET"])
    def crear_rodaje():
        matricula = request.form["matricula"]
        if db.session.query(Rodaje).filter_by(matricula=matricula, activo=True).all():
            rodaje = Rodaje(matricula=request.form["matricula"],
                            pago_rodaje=datetime.strptime(request.form["pago_rodaje"], '%Y-%m-%d'),
                            venc_rodaje=datetime.strptime(request.form["venc_rodaje"], '%Y-%m-%d'),
                            obs_rodaje=request.form["obs_rodaje"],
                            imp_rodaje=request.form["imp_rodaje"])
            pasar_false = db.session.query(Rodaje).filter_by(matricula=matricula, activo=True).first()
            pasar_false.activo = False
            db.session.add(rodaje)
            db.session.commit()
            return redirect(url_for('lista_rodajes'))

        if not db.session.query(Rodaje).filter_by(matricula=matricula, activo=True).all():
            rodaje = Rodaje(matricula=request.form["matricula"],
                            pago_rodaje=datetime.strptime(request.form["pago_rodaje"], '%Y-%m-%d'),
                            venc_rodaje=datetime.strptime(request.form["venc_rodaje"], '%Y-%m-%d'),
                            obs_rodaje=request.form["obs_rodaje"],
                            imp_rodaje=request.form["imp_rodaje"])
            db.session.add(rodaje)
            db.session.commit()
            return redirect(url_for('lista_rodajes'))

        else:
            matriculas = db.session.query(Vehiculo.matricula).all()
            return render_template("crear_rodaje.html", lista_matriculas=matriculas)
