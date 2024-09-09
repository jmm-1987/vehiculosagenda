from flask import render_template, redirect, url_for, request
from flask_login import login_required
import db
from datetime import datetime
from models import Itv, Vehiculo
import json


def register_itv_routes(app):
    @app.route('/itv')
    @login_required
    def lista_itv():
        todas_itv = db.session.query(Itv).filter(Itv.activo == True).all()
        return render_template('itv.html', lista_itv=todas_itv)

    @app.route('/itv_todas')
    def lista_itv_todas():
        todas_itv = db.session.query(Itv).all()
        return render_template('itv.html', lista_itv=todas_itv)


    @app.route('/formulario_itv')
    def formulario_itv():
        matriculas = db.session.query(Vehiculo.matricula).all()
        return render_template("crear_itv.html", lista_matriculas=matriculas)

    @app.route("/borrar_itv/<id>", methods=["POST", "GET"])
    def borrar_itv(id):
        registro_borrar = db.session.query(Itv).filter_by(id=id).first()
        db.session.delete(registro_borrar)
        db.session.commit()
        return redirect(url_for('lista_itv'))

    @app.route("/crear_itv", methods=["POST"])
    def crear_itv():
        matricula=request.form["matricula"]
        #Si existe registro con activo TRUE
        anterior = db.session.query(Itv).filter_by(matricula=matricula, activo=True).all()
        if anterior:
            if request.form["cita_itv"]:
                cita_itv = datetime.strptime(request.form["cita_itv"], '%Y-%m-%d')
            else:
                cita_itv = None
            itv = Itv(matricula=request.form["matricula"],
                      fecha_itv=datetime.strptime(request.form["fecha_itv"], '%Y-%m-%d'),
                      venc_itv=datetime.strptime(request.form["venc_itv"], '%Y-%m-%d'),
                      cita_itv = cita_itv,
                      obs_itv=request.form["obs_itv"])
            pasar_false = db.session.query(Itv).filter_by(matricula=matricula, activo=True).first()
            pasar_false.activo = False
            clave = "clave"
            db.session.add(itv)
            db.session.commit()

            #Hay pasar el mensaje de confirmación adecuado
            return redirect(url_for('lista_itv', clave=clave))
        if not db.session.query(Itv).filter_by(matricula=matricula, activo=True).all():
            itv = Itv(matricula=request.form["matricula"],
                      fecha_itv=datetime.strptime(request.form["fecha_itv"], '%Y-%m-%d'),
                      venc_itv=datetime.strptime(request.form["venc_itv"], '%Y-%m-%d'),
                      cita_itv=datetime.strptime(request.form["cita_itv"], '%Y-%m-%d'),
                      obs_itv=request.form["obs_itv"])
            db.session.add(itv)
            db.session.commit()
            return redirect(url_for('lista_itv'))
        else:
            matriculas = db.session.query(Vehiculo.matricula).all()
            return render_template("crear_itv.html", lista_matriculas=matriculas)
