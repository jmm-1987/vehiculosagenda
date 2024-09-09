from flask import render_template, request, redirect, url_for
from flask_login import login_required
import db
from models import Vehiculo

def register_vehiculos_routes(app):
    @app.route('/vehiculos')
    @login_required
    def lista_vehiculos():
        todos_los_vehiculos = db.session.query(Vehiculo).filter(Vehiculo.activo == True).all()
        return render_template('vehiculos.html', lista_vehiculos=todos_los_vehiculos)

    @app.route('/vehiculos_todos')
    def lista_vehiculos_todos():
        todos_vehiculos = db.session.query(Vehiculo).all()
        return render_template('vehiculos.html', lista_vehiculos=todos_vehiculos)

    @app.route('/formulario_vehiculos')
    def formulario():
        return render_template("crear_vehiculo.html")

    @app.route('/crear_vehiculo', methods=['POST'])
    def crear_vehiculo():
        vehiculo = Vehiculo(matricula=request.form['matricula'],
                            alias=request.form['alias'],
                            tipo=request.form['tipo'])
        db.session.add(vehiculo)
        db.session.commit()
        return redirect(url_for('lista_vehiculos'))

    @app.route('/inactivo_vehiculo/<id>', methods=['POST',"GET"])
    def inactivo(id):
        vehiculo = db.session.query(Vehiculo).filter_by(id=(id)).first()
        if vehiculo.activo == True:
            vehiculo.activo = False
        elif vehiculo.activo == False:
            vehiculo.activo = True
        db.session.commit()
        return redirect(url_for('lista_vehiculos'))

    @app.route('/form_editar_vehiculo/<id>')
    def edicion_vehiculo(id):
        veh_editar = db.session.query(Vehiculo).filter_by(id=(id)).first()
        veh_editar_matricula = veh_editar.matricula
        veh_editar_alias = veh_editar.alias
        veh_editar_tipo = veh_editar.tipo


        return render_template("form_editar_vehiculo.html", veh_editar=veh_editar,
                               veh_editar_matricula=veh_editar_matricula,
                               veh_editar_alias=veh_editar_alias,
                               veh_editar_tipo=veh_editar_tipo)

    @app.route("/modificar_vehiculo", methods=['POST'])
    def modificar_vehiculo():
        id = request.form["id"]
        matricula = request.form["matricula_ant"]
        alias = request.form["alias_new"]
        tipo = request.form["tipo_new"]
        vehiculo_mod = db.session.query(Vehiculo).filter_by(id=(id)).first()
        vehiculo_mod.matricula = matricula
        vehiculo_mod.alias = alias
        vehiculo_mod.tipo = tipo
        db.session.commit()
        todos_vehiculos = db.session.query(Vehiculo).all()
        return render_template("vehiculos.html", lista_vehiculos=todos_vehiculos)
