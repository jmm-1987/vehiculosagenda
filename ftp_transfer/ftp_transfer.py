from flask import render_template, request, redirect, url_for, flash, jsonify
import ftplib
from io import BytesIO
import os
from apscheduler.schedulers.background import BackgroundScheduler
import datetime

def register_ftp_transfer_routes(app):
    @app.route('/ftp_transfer/estado_scheduler')
    def estado_scheduler():
        """Endpoint para verificar el estado del scheduler"""
        global _scheduler
        try:
            if _scheduler is None:
                return jsonify({
                    'scheduler_iniciado': False,
                    'mensaje': 'Scheduler no ha sido iniciado'
                })
            
            jobs = _scheduler.get_jobs()
            job_info = []
            for job in jobs:
                job_info.append({
                    'id': job.id,
                    'next_run_time': str(job.next_run_time) if job.next_run_time else None,
                    'func': job.func.__name__ if hasattr(job.func, '__name__') else str(job.func)
                })
            
            return jsonify({
                'scheduler_iniciado': True,
                'scheduler_running': _scheduler.running if _scheduler else False,
                'jobs': job_info,
                'total_jobs': len(jobs)
            })
        except Exception as e:
            return jsonify({
                'error': str(e),
                'scheduler_iniciado': False
            })
    
    @app.route('/ftp_transfer/ejecutar_ahora')
    def ejecutar_tarea_ahora():
        """Endpoint para ejecutar la tarea manualmente (para pruebas)"""
        try:
            tarea_programada()
            return jsonify({
                'success': True,
                'mensaje': 'Tarea ejecutada manualmente'
            })
        except Exception as e:
            import traceback
            return jsonify({
                'success': False,
                'error': str(e),
                'traceback': traceback.format_exc()
            })
    
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
        try:
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

                # Solo agregar si tiene datos válidos
                if ftp_dest and username_dest and password_dest and prefix_dest and directory_dest:
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
        except Exception as e:
            import traceback
            error_msg = f"Error en iniciar_transferencia_route: {str(e)}"
            print(error_msg)
            print(traceback.format_exc())
            logs = [f"Error: {error_msg}"]
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
            return render_template('ftp_transfer.html', origen=origen, conexiones=lista_conexiones, logs=logs)

def iniciar_transferencia(datos):
    origen = datos['origen']
    destinos = datos['destinos']
    logs = []
    MAX_ARCHIVOS = 20
    archivos_transferidos = 0

    # Validar datos de origen
    if not origen or not origen.get('ftp') or not origen.get('username') or not origen.get('password') or not origen.get('directory'):
        logs.append("Error: Faltan datos del servidor de origen")
        return logs
    
    # Mostrar información de configuración al inicio
    logs.append("=" * 60)
    logs.append("CONFIGURACIÓN DE TRANSFERENCIA FTP")
    logs.append("=" * 60)

    try:
        logs.append(f"=== INFORMACIÓN DE CONEXIÓN ORIGEN ===")
        logs.append(f"Servidor FTP: {origen['ftp']}")
        logs.append(f"Usuario: {origen['username']}")
        logs.append(f"DIRECTORIO DE ORIGEN: {origen['directory']}")
        logs.append(f"========================================")
        
        logs.append(f"Conectando al servidor origen: {origen['ftp']}")
        ftp_origen = ftplib.FTP(origen['ftp'])
        ftp_origen.login(origen['username'], origen['password'])
        
        # Verificar directorio actual antes de cambiar
        pwd_antes = ftp_origen.pwd()
        logs.append(f"Directorio actual antes de cambiar: {pwd_antes}")
        
        # Cambiar al directorio de origen
        logs.append(f"Cambiando al directorio: {origen['directory']}")
        try:
            ftp_origen.cwd(origen['directory'])
        except Exception as e_cwd:
            logs.append(f"ERROR al cambiar al directorio {origen['directory']}: {str(e_cwd)}")
            logs.append("Intentando listar directorios disponibles...")
            try:
                directorios = ftp_origen.nlst()
                logs.append(f"Directorios/carpetas en el directorio actual: {directorios[:10]}")  # Primeros 10
            except:
                pass
            raise e_cwd
        
        # Verificar que el cambio fue exitoso
        pwd_despues = ftp_origen.pwd()
        logs.append(f"Directorio actual después de cambiar: {pwd_despues}")
        
        # Intentar listar archivos con diferentes métodos
        archivos_origen = []
        
        # Método 1: nlst() - puede fallar en algunos servidores
        try:
            archivos_nlst = ftp_origen.nlst()
            logs.append(f"nlst() encontró {len(archivos_nlst)} elementos")
            # Filtrar solo archivos (excluir directorios que empiezan con punto o son nombres especiales)
            archivos_nlst = [f for f in archivos_nlst if f and not f.startswith('.') and f not in ['.', '..']]
            archivos_origen = archivos_nlst
        except Exception as e_nlst:
            logs.append(f"Error con nlst(): {str(e_nlst)}")
        
        # Si nlst() no funcionó o devolvió pocos archivos, intentar con retrlines
        if len(archivos_origen) == 0:
            try:
                logs.append("Intentando listar con retrlines('NLST')...")
                archivos_list = []
                ftp_origen.retrlines('NLST', archivos_list.append)
                # Filtrar solo archivos válidos
                archivos_list = [f for f in archivos_list if f and not f.startswith('.') and f not in ['.', '..']]
                archivos_origen = archivos_list
                logs.append(f"retrlines('NLST') encontró {len(archivos_origen)} archivos")
            except Exception as e_retr:
                logs.append(f"Error con retrlines('NLST'): {str(e_retr)}")
        
        # Si aún no hay archivos, intentar con dir() y parsear
        if len(archivos_origen) == 0:
            try:
                logs.append("Intentando listar con dir()...")
                archivos_dir = []
                ftp_origen.retrlines('LIST', archivos_dir.append)
                # Parsear la salida de LIST para extraer nombres de archivos
                archivos_parseados = []
                for linea in archivos_dir:
                    # El formato típico es: -rw-r--r-- 1 user group size date time filename
                    partes = linea.split()
                    if len(partes) >= 9:
                        nombre_archivo = ' '.join(partes[8:])  # El nombre puede tener espacios
                        if nombre_archivo and not nombre_archivo.startswith('.'):
                            archivos_parseados.append(nombre_archivo)
                archivos_origen = archivos_parseados
                logs.append(f"dir() encontró {len(archivos_origen)} archivos")
            except Exception as e_dir:
                logs.append(f"Error con dir(): {str(e_dir)}")
        
        # Mostrar algunos ejemplos de archivos encontrados
        if len(archivos_origen) > 0:
            logs.append(f"Archivos encontrados en origen: {len(archivos_origen)}")
            # Mostrar primeros 5 archivos como ejemplo
            ejemplos = archivos_origen[:5]
            logs.append(f"Ejemplos de archivos: {', '.join(ejemplos)}")
        else:
            logs.append(f"ADVERTENCIA: No se encontraron archivos en {origen['directory']}")
            logs.append("Verifica que el directorio sea correcto y que tenga archivos")

        for destino in destinos:
            # Validar datos de destino
            if not destino or not destino.get('ftp') or not destino.get('username') or not destino.get('password') or not destino.get('directory') or not destino.get('prefix'):
                logs.append(f"Error: Faltan datos del destino. Saltando...")
                continue

            try:
                logs.append(f"Conectando al destino: {destino['ftp']} - {destino['directory']}")
                ftp_dest = ftplib.FTP(destino['ftp'])
                ftp_dest.login(destino['username'], destino['password'])
                ftp_dest.cwd(destino['directory'])

                for archivo in archivos_origen:
                    if archivo.startswith(destino['prefix']):
                        if archivos_transferidos >= MAX_ARCHIVOS:
                            logs.append("Límite de 20 archivos alcanzado. Proceso detenido.")
                            ftp_dest.quit()
                            ftp_origen.quit()
                            return logs

                        try:
                            logs.append(f"Transfiriendo {archivo} a {destino['directory']} en {destino['ftp']}")
                            file_buffer = BytesIO()
                            ftp_origen.retrbinary(f'RETR {archivo}', file_buffer.write)
                            file_buffer.seek(0)
                            ftp_dest.storbinary(f'STOR {archivo}', file_buffer)
                            logs.append(f"{archivo} transferido con éxito a {destino['directory']} en {destino['ftp']}")
                            ftp_origen.delete(archivo)
                            logs.append(f"{archivo} eliminado del servidor de origen.")
                            archivos_transferidos += 1
                        except Exception as e_archivo:
                            logs.append(f"Error al transferir {archivo}: {str(e_archivo)}")
                            continue

                ftp_dest.quit()
            except Exception as e_destino:
                logs.append(f"Error conectando al destino {destino.get('ftp', 'desconocido')}: {str(e_destino)}")
                continue

        ftp_origen.quit()
        logs.append(f"Transferencia completada. Total de archivos transferidos: {archivos_transferidos}")

    except Exception as e:
        error_msg = f"Error durante la transferencia: {str(e)}"
        logs.append(error_msg)
        import traceback
        logs.append(f"Detalles: {traceback.format_exc()}")

    return logs


def cargar_config_ftp():
    """
    Devuelve siempre la configuración por defecto (la misma que se usa en la ejecución manual).
    No lee el archivo JSON.
    """
    # Configuración por defecto (la misma que se usa en ejecución manual)
    config_default = {
        "origen": {
            "ftp": "ftpclientes.nereid.es",
            "username": "ne4ld1tr43xSurp4q",
            "password": "J8QP123(A2e",
            "directory": "XPOsalidas"
        },
        "destinos": [
            {
                "ftp": "ftpclientes.nereid.es",
                "username": "ne4ld1tr43xSurp4q",
                "password": "J8QP123(A2e",
                "prefix": "DSEL",
                "directory": "PODSalidasXPO/POD"
            },
            {
                "ftp": "ftpclientes.nereid.es",
                "username": "ne4ld1tr43xSurp4q",
                "password": "J8QP123(A2e",
                "prefix": "GGSS",
                "directory": "PODSalidasXPO/PRIVADO"
            },
            {
                "ftp": "ftpclientes.nereid.es",
                "username": "ne4ld1tr43xSurp4q",
                "password": "J8QP123(A2e",
                "prefix": "VARI",
                "directory": "PODSalidasXPO/PRIVADO"
            },
            {
                "ftp": "ftpclientes.nereid.es",
                "username": "ne4ld1tr43xSurp4q",
                "password": "J8QP123(A2e",
                "prefix": "DADR",
                "directory": "PODSalidasXPO/PRIVADO"
            },
            {
                "ftp": "ftpclientes.nereid.es",
                "username": "ne4ld1tr43xSurp4q",
                "password": "J8QP123(A2e",
                "prefix": "ATRA",
                "directory": "PODSalidasXPO/POD"
            },
            {
                "ftp": "ftpclientes.nereid.es",
                "username": "ne4ld1tr43xSurp4q",
                "password": "J8QP123(A2e",
                "prefix": "DFIR",
                "directory": "PODSalidasXPO/POD"
            },
            {
                "ftp": "ftpclientes.nereid.es",
                "username": "ne4ld1tr43xSurp4q",
                "password": "J8QP123(A2e",
                "prefix": "DALB",
                "directory": "PODSalidasXPO/POD"
            },
            {
                "ftp": "ftpclientes.nereid.es",
                "username": "ne4ld1tr43xSurp4q",
                "password": "J8QP123(A2e",
                "prefix": "POD",
                "directory": "PODSalidasXPO/POD"
            },
            {
                "ftp": "ftpclientes.nereid.es",
                "username": "ne4ld1tr43xSurp4q",
                "password": "J8QP123(A2e",
                "prefix": "CONS",
                "directory": "PODSalidasXPO/POD"
            },
            {
                "ftp": "ftpclientes.nereid.es",
                "username": "ne4ld1tr43xSurp4q",
                "password": "J8QP123(A2e",
                "prefix": "EREP",
                "directory": "PODSalidasXPO/POD"
            },
            {
                "ftp": "ftpclientes.nereid.es",
                "username": "ne4ld1tr43xSurp4q",
                "password": "J8QP123(A2e",
                "prefix": "MANI",
                "directory": "PODSalidasXPO/POD"
            },
            {
                "ftp": "ftpclientes.nereid.es",
                "username": "ne4ld1tr43xSurp4q",
                "password": "J8QP123(A2e",
                "prefix": "INCC",
                "directory": "PODSalidasXPO/INC"
            },
            {
                "ftp": "ftpclientes.nereid.es",
                "username": "ne4ld1tr43xSurp4q",
                "password": "J8QP123(A2e",
                "prefix": "INCB",
                "directory": "PODSalidasXPO/INC"
            },
            {
                "ftp": "ftpclientes.nereid.es",
                "username": "ne4ld1tr43xSurp4q",
                "password": "J8QP123(A2e",
                "prefix": "DIMG",
                "directory": "PODSalidasXPO/INC"
            }
        ]
    }
    return config_default


def tarea_programada():
    try:
        import sys
        print("=" * 50, file=sys.stderr)
        print("============== INICIO DE TAREA PROGRAMADA ==============", file=sys.stderr)
        print(f"Hora de inicio: {datetime.datetime.now()}", file=sys.stderr)
        print(f"PID del proceso: {os.getpid()}", file=sys.stderr)
        
        datos = cargar_config_ftp()
        print("Ejecutando tarea programada...", file=sys.stderr)
        print(f"Configuración cargada: origen={datos.get('origen', {}).get('ftp', 'N/A')}, directorio={datos.get('origen', {}).get('directory', 'N/A')}, destinos={len(datos.get('destinos', []))}", file=sys.stderr)
        logs = iniciar_transferencia(datos)
        for log in logs:
            print(log, file=sys.stderr)

        print(f"Hora de finalización: {datetime.datetime.now()}", file=sys.stderr)
        print("=============== FIN DE TAREA PROGRAMADA ================", file=sys.stderr)
        print("=" * 50, file=sys.stderr)
    except Exception as e:
        import traceback
        print(f"ERROR CRÍTICO en tarea_programada: {str(e)}", file=sys.stderr)
        print(traceback.format_exc(), file=sys.stderr)

# Variable global para almacenar el scheduler
_scheduler = None

def iniciar_scheduler():
    global _scheduler
    try:
        if _scheduler is not None and _scheduler.running:
            print("Scheduler ya está corriendo. No se reinicia.")
            return
        
        import sys
        print(f"Iniciando scheduler... PID: {os.getpid()}", file=sys.stderr)
        _scheduler = BackgroundScheduler(daemon=False)
        _scheduler.add_job(
            tarea_programada,
            'interval',
            minutes=30,
            id='tarea_ftp_transfer',
            replace_existing=True,
            max_instances=1,
            coalesce=True,
            next_run_time=datetime.datetime.now() + datetime.timedelta(minutes=30)
        )
        _scheduler.start()
        print(f"Scheduler iniciado correctamente. Tarea programada cada 30 minutos. PID: {os.getpid()}", file=sys.stderr)
        print(f"Estado del scheduler: running={_scheduler.running}", file=sys.stderr)
        
        # Verificar que el job está programado
        jobs = _scheduler.get_jobs()
        print(f"Jobs programados: {len(jobs)}", file=sys.stderr)
        for job in jobs:
            print(f"  - Job ID: {job.id}, Próxima ejecución: {job.next_run_time}", file=sys.stderr)
            
    except Exception as e:
        import traceback
        print(f"Error al iniciar scheduler: {e}", file=sys.stderr)
        print(traceback.format_exc(), file=sys.stderr)


