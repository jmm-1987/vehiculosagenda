from flask import render_template, redirect, url_for, request
from flask_login import login_required
import db
from datetime import datetime
from models import Tacografo,Vehiculo

def register_tacografos_routes(app):
    @app.route('/tacografos')
    @login_required
    def lista_tacografos():
        todos_tacografos = db.session.query(Tacografo).filter(Tacografo.activo == True).all()
        return render_template('tacografos.html', lista_tacografos = todos_tacografos)

    @app.route('/tacografos_todos')
    def lista_tacografos_todos():
        todos_tacografos = db.session.query(Tacografo).all()
        return render_template('tacografos.html', lista_tacografos=todos_tacografos)

    @app.route('/formulario_tacografo')
    def formulario_tacografo():
        matriculas = db.session.query(Vehiculo.matricula).filter(Vehiculo.tipo =="camion").all()
        return render_template("crear_tacografo.html", lista_matriculas=matriculas)

    @app.route("/borrar_tacografo/<id>", methods=["POST", "GET"])
    def borrar_tacografo(id):
        registro_borrar = db.session.query(Tacografo).filter_by(id=id).first()
        db.session.delete(registro_borrar)
        db.session.commit()
        return redirect(url_for('lista_tacografos'))

    @app.route("/crear_tacografo", methods=["POST", "GET"])
    def crear_tacografo():
        matricula = request.form["matricula"]
        if db.session.query(Tacografo).filter_by(matricula=matricula, activo=True).all():
            tacografo = Tacografo(matricula=request.form["matricula"],
                                rev_tacografo=datetime.strptime(request.form["rev_tacografo"], '%Y-%m-%d'),
                                venc_tacografo=datetime.strptime(request.form["venc_tacografo"], '%Y-%m-%d'),
                                obs_tacografo=request.form["obs_tacografo"])
            pasar_false = db.session.query(Tacografo).filter_by(matricula=matricula, activo=True).first()
            pasar_false.activo = False
            db.session.add(tacografo)
            db.session.commit()
            return redirect(url_for('lista_tacografos'))

        if not db.session.query(Tacografo).filter_by(matricula=matricula, activo=True).all():
            tacografo = Tacografo(matricula=request.form["matricula"],
                                  rev_tacografo=datetime.strptime(request.form["rev_tacografo"], '%Y-%m-%d'),
                                  venc_tacografo=datetime.strptime(request.form["venc_tacografo"], '%Y-%m-%d'),
                                  obs_tacografo=request.form["obs_tacografo"])
            db.session.add(tacografo)
            db.session.commit()
            return redirect(url_for('lista_tacografos'))

        else:
            matriculas = db.session.query(Vehiculo.matricula).all()
            return render_template("crear_tacografo.html", lista_matriculas=matriculas)