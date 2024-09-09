from flask import render_template, redirect, url_for, request
from flask_login import login_required
import db
from datetime import datetime
from models import Taller, Vehiculo


def register_talleres_routes(app):
    @app.route('/talleres')
    def lista_talleres():
        matriculas = db.session.query(Vehiculo.matricula).filter(Vehiculo.activo == True).all()
        todos_talleres = db.session.query(Taller).order_by(Taller.fecha_visita.desc()).all()
        return render_template('talleres.html', lista_talleres=todos_talleres, lista_matriculas=matriculas)

    @app.route("/busqueda_matricula", methods=["POST", "GET"])
    def busqueda_matricula():
        matricula = request.form["matricula"]
        matriculas = db.session.query(Vehiculo.matricula).filter(Vehiculo.activo == True).all()
        talleres_mat = db.session.query(Taller).filter(Taller.matricula == matricula).all()
        return render_template('talleres.html', lista_talleres=talleres_mat, lista_matriculas=matriculas)


    @app.route('/formulario_taller')
    def formulario_taller():
        matriculas = db.session.query(Vehiculo.matricula).all()
        return render_template("crear_taller.html", lista_matriculas=matriculas)

    @app.route("/crear_taller", methods=["POST", "GET"])
    def crear_taller():
        fecha_entrega_str = request.form.get("fecha_entrega")
        if fecha_entrega_str:
            fecha_entrega = datetime.strptime(fecha_entrega_str, '%Y-%m-%d')
            activo = False
        else:
            fecha_entrega = None
            activo = True
        taller = Taller(matricula=request.form["matricula"],
                    problema=request.form["problema"],
                    taller=request.form["taller"],
                    albaran=request.form["albaran"],
                    presupuesto=request.form["presupuesto"],
                    fecha_visita=datetime.strptime(request.form["fecha_visita"], '%Y-%m-%d'),
                    kilometros = request.form["kilometros"],
                    trabajos=request.form["trabajos"],
                    importe=request.form["importe"],
                    fecha_entrega = fecha_entrega,
                    activo = activo)

        db.session.add(taller)
        db.session.commit()
        return redirect(url_for('lista_talleres'))

    @app.route('/ver_taller/<id>')
    def ver_taller(id):
        taller_ver = db.session.query(Taller).filter_by(id=(id)).first()
        return render_template("ver_taller.html", taller_ver=taller_ver)

    @app.route("/borrar_taller/<id>", methods=["POST", "GET"])
    def borrar_taller(id):
        registro_borrar = db.session.query(Taller).filter_by(id=id).first()
        db.session.delete(registro_borrar)
        db.session.commit()
        return redirect(url_for('lista_talleres'))
