from flask import render_template, request, send_file
import db
import os
from models import Tacografo, Itv, Seguro, Rodaje, Taller, Vehiculo
from datetime import datetime
from io import BytesIO
import paramiko

# 🔐 Configuración FTP (idealmente poner en config segura)
FTP_HOST = "home613353667.1and1-data.host"
FTP_PORT = 22
FTP_USER = "acc1197626868"
FTP_PASSWORD = "924-Tx%20.2"  # ⚠️ Mejor usar app.config.get('FTP_PASSWORD')

def subir_a_sftp_contenido(fileobj, remote_filename):
    try:
        transport = paramiko.Transport((FTP_HOST, FTP_PORT))
        transport.connect(username=FTP_USER, password=FTP_PASSWORD)
        sftp = paramiko.SFTPClient.from_transport(transport)

        remote_path = f"vehiculos/{remote_filename}"
        sftp.putfo(fileobj, remote_path)

        sftp.close()
        transport.close()
        return True
    except Exception as e:
        print("Error subiendo por SFTP:", e)
        return False


def register_func_especiales_routes(app):
    @app.route("/subir_doc", methods=['POST'])
    def subir_doc():
        archivo = request.files['documento']
        id = request.form['id']
        clase = request.form['clase']
        ahora = datetime.now()
        ano_actual = str(ahora.year)
        dia = f"{ahora.day:02d}"
        mes = f"{ahora.month:02d}"
        mensaje = "Documento subido correctamente"

        file_extension = os.path.splitext(archivo.filename)[1]
        in_memory_file = BytesIO()
        archivo.save(in_memory_file)
        in_memory_file.seek(0)

        if clase == "Tacografo":
            consulta = db.session.query(Tacografo).filter_by(id=id).first()
            if consulta:
                filename = consulta.matricula + "TAC" + ano_actual + file_extension
                consulta.nombre_doc = filename

        elif clase == "Itv":
            consulta = db.session.query(Itv).filter_by(id=id).first()
            if consulta:
                filename = consulta.matricula + "ITV" + ano_actual + file_extension
                consulta.nombre_doc = filename

        elif clase == "Seguro":
            consulta = db.session.query(Seguro).filter_by(id=id).first()
            if consulta:
                filename = consulta.matricula + "SEGURO" + ano_actual + file_extension
                consulta.nombre_doc = filename

        elif clase == "Rodaje":
            consulta = db.session.query(Rodaje).filter_by(id=id).first()
            if consulta:
                filename = consulta.matricula + "RODAJE" + ano_actual + file_extension
                consulta.nombre_doc = filename

        elif clase == "Taller":
            consulta = db.session.query(Taller).filter_by(id=id).first()
            if consulta:
                filename = consulta.matricula + "TALLER" + dia + mes + ano_actual + file_extension
                consulta.nombre_doc = filename

        elif clase == "ficha_tecnica":
            consulta = db.session.query(Vehiculo).filter_by(id=id).first()
            if consulta:
                filename = consulta.matricula + "FICHA_TECNICA" + file_extension
                consulta.doc_ficha = filename

        elif clase == "permiso":
            consulta = db.session.query(Vehiculo).filter_by(id=id).first()
            if consulta:
                filename = consulta.matricula + "PERMISO" + file_extension
                consulta.doc_permiso = filename

        else:
            return "Clase no válida", 400

        # Subir al FTP
        if consulta:
            subido = subir_a_sftp_contenido(in_memory_file, filename)
            if not subido:
                return "Error al subir el archivo al FTP", 500
            db.session.commit()

            # Redireccionar según clase
            if clase == "Tacografo":
                return render_template("tacografos.html", lista_tacografos=db.session.query(Tacografo).all(), mensaje=mensaje)
            elif clase == "Itv":
                return render_template("itv.html", lista_itv=db.session.query(Itv).all(), mensaje=mensaje)
            elif clase == "Seguro":
                return render_template("seguros.html", lista_seguros=db.session.query(Seguro).all(), mensaje=mensaje)
            elif clase == "Rodaje":
                return render_template("rodajes.html", lista_rodajes=db.session.query(Rodaje).all(), mensaje=mensaje)
            elif clase == "Taller":
                return render_template("talleres.html", lista_talleres=db.session.query(Taller).all(), mensaje=mensaje)
            elif clase in ["ficha_tecnica", "permiso"]:
                return render_template("vehiculos.html", lista_vehiculos=db.session.query(Vehiculo).all(), mensaje=mensaje)

        return "Error al procesar el documento", 500

    @app.route('/ver_documento_vehiculo/<filename>')
    def ver_documento_vehiculo(filename):
        host = "home613353667.1and1-data.host"
        port = 22
        username = "acc1197626868"
        password = "924-Tx%20.2"  # Mejor desde config segura

        try:
            transport = paramiko.Transport((host, port))
            transport.connect(username=username, password=password)
            sftp = paramiko.SFTPClient.from_transport(transport)

            remote_path = f"vehiculos/{filename}"
            file_io = BytesIO()
            sftp.getfo(remote_path, file_io)
            file_io.seek(0)

            sftp.close()
            transport.close()

            return send_file(file_io, download_name=filename, as_attachment=False)

        except Exception as e:
            return f"Error al acceder al documento: {e}", 500
