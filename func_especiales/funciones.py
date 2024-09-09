from flask import render_template, request
import db
import os
from models import Tacografo, Itv, Seguro, Rodaje, Taller, Vehiculo, Transpaleta
from datetime import datetime


def register_func_especiales_routes(app):
    @app.route("/subir_doc", methods=['POST'])
    def subir_doc():
        archivo = request.files['documento']
        filename = archivo.filename
        #subida_archivo = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        #archivo.save(subida_archivo)
        id = request.form['id']
        ano_actual = str(datetime.now().year)
        dia = str(datetime.now().day)
        mes = str(datetime.now().month)
        mensaje = "Documento subido correctamente"
        if request.form['clase'] == "Tacografo":
            consulta = db.session.query(Tacografo).filter_by(id=(id)).first()
            if consulta:
                file_extension = os.path.splitext(archivo.filename)[1]
                filename = consulta.matricula + "TAC" + ano_actual + file_extension
                consulta.nombre_doc = filename
                subida_archivo = os.path.join(app.config['UPLOAD_FOLDER'], consulta.nombre_doc)
                archivo.save(subida_archivo)
                db.session.commit()
                todos_tacografos = db.session.query(Tacografo).all()
                return render_template('tacografos.html', lista_tacografos = todos_tacografos, mensaje=mensaje)
        elif request.form['clase'] == "Itv":
            consulta = db.session.query(Itv).filter_by(id=(id)).first()
            if consulta:
                file_extension = os.path.splitext(archivo.filename)[1]
                filename = consulta.matricula + "ITV" + ano_actual + file_extension
                consulta.nombre_doc = filename
                subida_archivo = os.path.join(app.config['UPLOAD_FOLDER'], consulta.nombre_doc)
                archivo.save(subida_archivo)
                db.session.commit()
                todas_itv = db.session.query(Itv).all()
                return render_template('itv.html', lista_itv = todas_itv, mensaje=mensaje)
        elif request.form['clase'] == "Seguro":
            consulta = db.session.query(Seguro).filter_by(id=(id)).first()
            if consulta:
                file_extension = os.path.splitext(archivo.filename)[1]
                filename = consulta.matricula + "SEGURO" + ano_actual + file_extension
                consulta.nombre_doc = filename
                subida_archivo = os.path.join(app.config['UPLOAD_FOLDER'], consulta.nombre_doc)
                archivo.save(subida_archivo)
                db.session.commit()
                todos_seguros = db.session.query(Seguro).all()
                return render_template('seguros.html', lista_seguros = todos_seguros, mensaje=mensaje)
        elif request.form['clase'] == "Rodaje":
            consulta = db.session.query(Rodaje).filter_by(id=(id)).first()
            if consulta:
                file_extension = os.path.splitext(archivo.filename)[1]
                filename = consulta.matricula + "RODAJE" + ano_actual + file_extension
                consulta.nombre_doc = filename
                subida_archivo = os.path.join(app.config['UPLOAD_FOLDER'], consulta.nombre_doc)
                archivo.save(subida_archivo)
                db.session.commit()
                todos_rodajes = db.session.query(Rodaje).all()
                return render_template('rodajes.html', lista_rodajes = todos_rodajes, mensaje=mensaje)
        elif request.form['clase'] == "Taller":
            consulta = db.session.query(Taller).filter_by(id=(id)).first()
            if consulta:
                file_extension = os.path.splitext(archivo.filename)[1]
                filename = consulta.matricula + "TALLER" + dia + mes + ano_actual + file_extension
                consulta.nombre_doc = filename
                subida_archivo = os.path.join(app.config['UPLOAD_FOLDER'], consulta.nombre_doc)
                archivo.save(subida_archivo)
                db.session.commit()
                todos_talleres = db.session.query(Taller).all()
                return render_template('talleres.html', lista_talleres = todos_talleres, mensaje=mensaje)
        elif request.form['clase'] == "ficha_tecnica":
            consulta = db.session.query(Vehiculo).filter_by(id=(id)).first()
            if consulta:
                file_extension = os.path.splitext(archivo.filename)[1]
                filename = consulta.matricula + "FICHA_TECNICA" + file_extension
                consulta.doc_ficha = filename
                subida_archivo = os.path.join(app.config['UPLOAD_FOLDER'], consulta.doc_ficha)
                archivo.save(subida_archivo)
                db.session.commit()
                todos_vehiculos = db.session.query(Vehiculo).all()
                return render_template('vehiculos.html', lista_vehiculos = todos_vehiculos, mensaje=mensaje)
        elif request.form['clase'] == "permiso":
            consulta = db.session.query(Vehiculo).filter_by(id=(id)).first()
            if consulta:
                file_extension = os.path.splitext(archivo.filename)[1]
                filename = consulta.matricula + "PERMISO" + file_extension
                consulta.doc_permiso = filename
                subida_archivo = os.path.join(app.config['UPLOAD_FOLDER'], consulta.doc_permiso)
                archivo.save(subida_archivo)
                db.session.commit()
                todos_vehiculos = db.session.query(Vehiculo).all()
                return render_template('vehiculos.html', lista_vehiculos = todos_vehiculos, mensaje=mensaje)
