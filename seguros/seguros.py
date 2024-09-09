from flask import render_template, redirect, url_for, request
from flask_login import login_required
import db
from datetime import datetime
from models import Seguro, Vehiculo

def register_seguros_routes(app):
    @app.route('/seguros')
    @login_required
    def lista_seguros():
        todos_seguros = db.session.query(Seguro).filter(Seguro.activo == True).all()
        return render_template('seguros.html', lista_seguros=todos_seguros)

    @app.route('/seguros_todos')
    def lista_seguros_todos():
        todos_seguros = db.session.query(Seguro).all()
        return render_template('seguros.html', lista_seguros=todos_seguros)


    @app.route('/formulario_seguro')
    def formulario_seguro():
        matriculas = db.session.query(Vehiculo.matricula).all()
        return render_template("crear_seguro.html", lista_matriculas=matriculas)

    @app.route("/borrar_seguro/<id>", methods=["POST", "GET"])
    def borrar_seguro(id):
        registro_borrar = db.session.query(Seguro).filter_by(id=id).first()
        db.session.delete(registro_borrar)
        db.session.commit()
        return redirect(url_for('lista_seguros'))

    @app.route("/crear_seguro", methods=["POST"])
    def crear_seguro():
        matricula = request.form["matricula"]
        # Si existe registro con activo TRUE
        #anterior = db.session.query(Seguro).filter_by(matricula=matricula, activo=True).all()
        if db.session.query(Seguro).filter_by(matricula=matricula, activo=True).all():
            seguro = Seguro(matricula=request.form["matricula"],
                            venc_seguro=datetime.strptime(request.form["venc_seguro"], '%Y-%m-%d'),
                            cia_seguro=request.form["cia_seguro"],
                            cob_seguro=request.form["cob_seguro"],
                            obs_seguro=request.form["obs_seguro"],
                            fra_seguro=request.form["fra_seguro"],
                            pri_seguro=request.form["pri_seguro"])
            pasar_false = db.session.query(Seguro).filter_by(matricula=matricula, activo=True).first()
            pasar_false.activo = False
            #clave = "clave"
            db.session.add(seguro)
            db.session.commit()
            return redirect(url_for('lista_seguros'))

        if not db.session.query(Seguro).filter_by(matricula=matricula, activo=True).all():
            seguro = Seguro(matricula=request.form["matricula"],
                            venc_seguro=datetime.strptime(request.form["venc_seguro"], '%Y-%m-%d'),
                            cia_seguro=request.form["cia_seguro"],
                            cob_seguro=request.form["cob_seguro"],
                            obs_seguro=request.form["obs_seguro"],
                            fra_seguro=request.form["fra_seguro"],
                            pri_seguro=request.form["pri_seguro"])
            db.session.add(seguro)
            db.session.commit()
            return redirect(url_for('lista_seguros'))

        else:
            matriculas = db.session.query(Vehiculo.matricula).all()
            return render_template("crear_seguro.html", lista_matriculas=matriculas)