from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user
import db
from models import Usuario
from permisos import MODULOS, USUARIO_FIJO, marcas_para_formulario, guardar_permisos_de_usuarios

def register_usuarios_routes(app):
    @app.route('/manager')
    @login_required
    def lista_usuarios():
        todos_usuarios = db.session.query(Usuario).order_by(Usuario.username).all()
        accesos = {}
        estados = {}
        for usuario in todos_usuarios:
            marcas, tipo = marcas_para_formulario(usuario.username)
            accesos[usuario.id] = marcas
            estados[usuario.id] = tipo
        return render_template(
            'manager.html',
            lista_usuarios=todos_usuarios,
            modulos=MODULOS,
            accesos=accesos,
            estados=estados,
            guardado=request.args.get('guardado'),
            editado=request.args.get('editado'),
            error=request.args.get('error'),
        )

    @app.route('/guardar_permisos', methods=['POST'])
    @login_required
    def guardar_permisos():
        seleccion = {}
        for raw_id in request.form.getlist('usuarios'):
            try:
                uid = int(raw_id)
            except (TypeError, ValueError):
                continue
            seleccion[uid] = set(request.form.getlist(f'perm_{uid}'))
        guardar_permisos_de_usuarios(seleccion)
        return redirect(url_for('lista_usuarios', guardado=1))

    @app.route('/formulario_usuario')
    @login_required
    def formulario_usuario():
        return render_template("crear_usuario.html")

    @app.route("/borrar_usuario/<id>", methods=["POST", "GET"])
    @login_required
    def borrar_usuario(id):
        registro_borrar = db.session.query(Usuario).filter_by(id=id).first()
        if registro_borrar is not None and (registro_borrar.username or '').strip().lower() != USUARIO_FIJO:
            db.session.delete(registro_borrar)
            db.session.commit()
        return redirect(url_for('lista_usuarios'))

    @app.route('/editar_usuario/<int:id>', methods=['POST'])
    @login_required
    def editar_usuario(id):
        registro = db.session.query(Usuario).filter_by(id=id).first()
        if registro is None or (registro.username or '').strip().lower() == USUARIO_FIJO:
            return redirect(url_for('lista_usuarios'))
        nombre = (request.form.get('usuario') or '').strip()
        password = request.form.get('password') or ''
        if not nombre or not password.strip():
            return redirect(url_for('lista_usuarios', error='vacio'))
        repetido = db.session.query(Usuario).filter(
            Usuario.username == nombre,
            Usuario.id != registro.id,
        ).first()
        if repetido is not None:
            return redirect(url_for('lista_usuarios', error='existe'))
        registro.username = nombre
        registro.password = password
        db.session.commit()
        return redirect(url_for('lista_usuarios', editado=1))

    @app.route("/crear_usuario", methods=["POST", "GET"])
    @login_required
    def crear_usuario():
        usuario = Usuario(username=request.form["usuario"],
                          password=request.form["password"])
        usuario.permisos = "[]"
        db.session.add(usuario)
        db.session.commit()
        return redirect(url_for('lista_usuarios'))

    @app.route('/ficheros')
    @login_required
    def ficheros():
        return render_template("ficheros.html")

