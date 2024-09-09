from flask import render_template, redirect, url_for, request
from flask_login import login_required
import db
from datetime import datetime
from models import Usuario

def register_usuarios_routes(app):
    @app.route('/manager')
    #@login_required
    def lista_usuarios():
        todos_usuarios = db.session.query(Usuario).all()
        return render_template('manager.html', lista_usuarios = todos_usuarios)

    @app.route('/formulario_usuario')
    def formulario_usuario():
        return render_template("crear_usuario.html")

    @app.route("/borrar_usuario/<id>", methods=["POST", "GET"])
    def borrar_usuario(id):
        registro_borrar = db.session.query(Usuario).filter_by(id=id).first()
        db.session.delete(registro_borrar)
        db.session.commit()
        return redirect(url_for('lista_usuarios'))

    @app.route("/crear_usuario", methods=["POST", "GET"])
    def crear_usuario():
        usuario = Usuario (username = request.form["usuario"],
                           password = request.form["password"])
        db.session.add(usuario)
        db.session.commit()
        return redirect(url_for('lista_usuarios'))

