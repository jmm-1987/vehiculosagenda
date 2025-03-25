from flask import render_template, request, redirect, url_for, flash
import ftplib
from io import BytesIO
import json
import os
from apscheduler.schedulers.background import BackgroundScheduler

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, '..', 'static', 'ftp_config.json')

def register_ftp_transfer_routes(app):
    @app.route('/ftp_transfer')
    def ftp_transfer():
        origen = ["ftpclientes.nereid.es", "ne4ld1tr43xSurp4q", "J8QP123(A2e", "XPOsalidas"]
        lista_conexiones = [
            ["ftpclientes.nereid.es", "ne4ld1tr43xSurp4q", "J8QP123(A2e", "DSEL", "PODSalidasXPO/POD"],
            ["ftpclientes.nereid.es", "ne4ld1tr43xSurp4q", "J8QP123(A2e", "GGSS", "PODSalidasXPO/PRIVADO"],
            ["ftpclientes.nereid.es", "ne4ld1tr43xSurp4q", "J8QP123(A2e", "VARI", "PODSalidasXPO/PRIVADO"],
            ["ftpclientes.nereid.es", "ne4ld1tr43xSurp4q", "J8QP123(A2e", "DADR", "PODSalidasXPO/PRIVADO"],
            ["ftpclientes.nereid.es", "ne4ld1tr43xSurp4q", "J8QP123(A2e", "ATRA", "PODSalidasXPO/POD"],
            ["ftpclientes.nereid.es", "ne4ld1tr43xSurp4q", "J8QP123(A2e", "DFIR", "PODSalidasXPO/POD"],
            ["ftpclientes.nereid.es", "ne4ld1tr43xSurp4q", "J8QP123(A2e", "DALB", "PODSalidasXPO/POD"],
            ["ftpclientes.nereid.es", "ne4ld1tr43xSurp4q", "J8QP123(A2e", "POD", "PODSalidasXPO/POD"],
            ["ftpclientes.nereid.es", "ne4ld1tr43xSurp4q", "J8QP123(A2e", "CONS", "PODSalidasXPO/POD"],
            ["ftpclientes.nereid.es", "ne4ld1tr43xSurp4q", "J8QP123(A2e", "EREP", "PODSalidasXPO/POD"],
            ["ftpclientes.nereid.es", "ne4ld1tr43xSurp4q", "J8QP123(A2e", "MANI", "PODSalidasXPO/POD"],
            ["ftpclientes.nereid.es", "ne4ld1tr43xSurp4q", "J8QP123(A2e", "INCC", "PODSalidasXPO/INC"],
            ["ftpclientes.nereid.es", "ne4ld1tr43xSurp4q", "J8QP123(A2e", "INCB", "PODSalidasXPO/INC"],
            ["ftpclientes.nereid.es", "ne4ld1tr43xSurp4q", "J8QP123(A2e", "DIMG", "PODSalidasXPO/INC"]
        ]
        return render_template('ftp_transfer.html', origen=origen, conexiones=lista_conexiones)

    @app.route('/volver', methods=['POST'])
    def volver_ftp_transfer():
        # Volver a cargar la página principal de ftp_transfer
        return redirect(url_for('ftp_transfer'))

    @app.route('/iniciar_transferencia', methods=['POST'])
    def iniciar_transferencia_route():
        ftp_origen = request.form.get('ftp_origen')
        username_origen = request.form.get('username_origen')
        password_origen = request.form.get('password_origen')
        directory_origen = request.form.get('directory_origen')

        lista_conexiones = []
        numero_conexiones = len(request.form) // 5

        for i in range(1, numero_conexiones + 1):
            ftp_dest = request.form.get(f'ftp_dest_{i}')
            username_dest = request.form.get(f'username_dest_{i}')
            password_dest = request.form.get(f'password_dest_{i}')
            prefix_dest = request.form.get(f'prefix_dest_{i}')
            directory_dest = request.form.get(f'directory_dest_{i}')

            lista_conexiones.append({
                'ftp': ftp_dest,
                'username': username_dest,
                'password': password_dest,
                'prefix': prefix_dest,
                'directory': directory_dest
            })

        logs = iniciar_transferencia({
            'origen': {
                'ftp': ftp_origen,
                'username': username_origen,
                'password': password_origen,
                'directory': directory_origen
            },
            'destinos': lista_conexiones
        })

        return render_template('ftp_transfer.html', origen=[ftp_origen, username_origen, password_origen, directory_origen], conexiones=lista_conexiones, logs=logs)

def iniciar_transferencia(datos):
    origen = datos['origen']
    destinos = datos['destinos']
    logs = []

    try:
        with ftplib.FTP(origen['ftp']) as ftp_origen:
            ftp_origen.login(origen['username'], origen['password'])
            ftp_origen.cwd(origen['directory'])
            archivos_origen = ftp_origen.nlst()

            for destino in destinos:
                with ftplib.FTP(destino['ftp']) as ftp_dest:
                    ftp_dest.login(destino['username'], destino['password'])
                    ftp_dest.cwd(destino['directory'])

                    for archivo in archivos_origen:
                        if archivo.startswith(destino['prefix']):
                            logs.append(f"Transferiendo {archivo} a {destino['directory']} en {destino['ftp']}")
                            file_buffer = BytesIO()
                            ftp_origen.retrbinary(f'RETR {archivo}', file_buffer.write)
                            file_buffer.seek(0)
                            ftp_dest.storbinary(f'STOR {archivo}', file_buffer)
                            logs.append(f"{archivo} transferido con éxito a {destino['directory']} en {destino['ftp']}")
                            ftp_origen.delete(archivo)
                            logs.append(f"{archivo} eliminado del servidor de origen.")
                        else:
                            logs.append(f"El archivo {archivo} no coincide con el prefijo {destino['prefix']}")

    except Exception as e:
        logs.append(f"Error durante la transferencia: {e}")

    return logs


def cargar_config_ftp():
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error cargando config: {e}")
        return None


def tarea_programada():
    datos = cargar_config_ftp()
    if datos:
        print("Ejecutando tarea programada...")
        logs = iniciar_transferencia(datos)
        for log in logs:
            print(log)
    else:
        print("No hay configuración disponible para ejecutar la tarea.")

def iniciar_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(tarea_programada, 'interval', hours=1)
    scheduler.start()


