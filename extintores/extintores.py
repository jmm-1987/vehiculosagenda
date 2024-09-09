from flask import render_template, redirect, url_for, request
from flask_login import login_required
import db
from models import Extintor, Vehiculo
from datetime import datetime

def register_extintores_routes(app):
    @app.route('/extintores')
    @login_required
    def lista_extintores():
        todos_extintores = db.session.query(Extintor).all()
        return render_template('extintores.html', lista_extintores=todos_extintores)

    @app.route('/formulario_extintor')
    def formulario_extintor():
        matriculas = db.session.query(Vehiculo.matricula).all()
        return render_template("crear_extintor.html", lista_matriculas=matriculas)

    @app.route("/borrar_extintor/<id>", methods=["POST", "GET"])
    def borrar_extintor(id):
        registro_borrar = db.session.query(Extintor).filter_by(id=id).first()
        db.session.delete(registro_borrar)
        db.session.commit()
        return redirect(url_for('lista_extintores'))

    @app.route("/crear_extintor", methods=["POST", "GET"])
    def crear_extintor():
        extintor = Extintor(matricula=request.form["matricula"],
                            id_ext=request.form["id_ext"],
                            ano_ext=request.form["ano_ext"],
                            rev_ext=datetime.strptime(request.form["rev_ext"], '%Y-%m-%d'),
                            venc_ret_ext=datetime.strptime(request.form["venc_ret_ext"], '%Y-%m-%d'),
                            venc_ext=datetime.strptime(request.form["venc_ext"], '%Y-%m-%d'),
                            obs_ext=request.form["obs_ext"])
        db.session.add(extintor)
        db.session.commit()
        return redirect(url_for('lista_extintores'))
