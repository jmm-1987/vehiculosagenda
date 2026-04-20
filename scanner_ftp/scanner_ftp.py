"""
Rutas para el scanner de códigos de barras y subida de imágenes a FTP
"""
from flask import render_template, request, jsonify, send_file
from flask_login import login_required, current_user
from .funciones_scanner import (
    subir_archivo_ftp, 
    validar_codigo_barras, 
    limpiar_nombre_archivo,
    guardar_imagen_temporal,
    limpiar_archivos_temporales,
    registrar_incidencia,
    conectar_sftp_backup,
    obtener_backup_local_root
)
import os
import io
import re
import time
from datetime import datetime

def register_scanner_ftp_routes(app):
    """Registra las rutas del scanner FTP"""
    
    @app.route('/scanner_clientes')
    @login_required
    def scanner_clientes():
        """Muestra la página con los 8 contenedores de clientes"""
        # Limpiar archivos temporales antiguos
        limpiar_archivos_temporales()
        return render_template('scanner_clientes.html')
    
    @app.route('/registro_incidencias_aldipod')
    @login_required
    def registro_incidencias_aldipod():
        """Muestra el registro de incidencias ALDIPOD"""
        import db
        from models import IncidenciaAldipod
        
        # Obtener el usuario actual
        usuario_actual = current_user.username if current_user.is_authenticated else ""
        
        # Actualizar incidencias existentes que no tengan ubicación
        incidencias_sin_ubicacion = db.session.query(IncidenciaAldipod).filter(
            (IncidenciaAldipod.ubicacion == None) | (IncidenciaAldipod.ubicacion == '')
        ).all()
        
        for incidencia in incidencias_sin_ubicacion:
            # Mapeo de usuarios a ubicaciones (mismo que en funciones_scanner.py)
            usuarios_merida = ['jmurillo', 'rocio', 'rep', 'oficina', 'almacen', 'fbonilla', 'jmgarcia']
            usuarios_navalmoral = ['repnav', 'yramos']
            
            if incidencia.usuario in usuarios_navalmoral:
                incidencia.ubicacion = 'Navalmoral'
            elif incidencia.usuario in usuarios_merida:
                incidencia.ubicacion = 'Mérida'
            else:
                incidencia.ubicacion = 'Mérida'  # Por defecto
        
        if incidencias_sin_ubicacion:
            db.session.commit()
            print(f"DEBUG: Actualizadas {len(incidencias_sin_ubicacion)} incidencias sin ubicación")
        
        # Filtrar incidencias según el usuario
        if usuario_actual in ['fbonilla', 'jmgarcia']:
            # Solo mostrar incidencias de Mérida
            incidencias = db.session.query(IncidenciaAldipod).filter(
                IncidenciaAldipod.ubicacion == 'Mérida'
            ).order_by(IncidenciaAldipod.fecha.desc()).all()
        elif usuario_actual == 'yramos':
            # Solo mostrar incidencias de Navalmoral
            incidencias = db.session.query(IncidenciaAldipod).filter(
                IncidenciaAldipod.ubicacion == 'Navalmoral'
            ).order_by(IncidenciaAldipod.fecha.desc()).all()
        else:
            # Para otros usuarios, mostrar todas las incidencias
            incidencias = db.session.query(IncidenciaAldipod).order_by(IncidenciaAldipod.fecha.desc()).all()
        
        return render_template('registro_incidencias_aldipod.html', incidencias=incidencias)
    
    @app.route('/incidencia_aldipod/comunicada', methods=['POST'])
    @login_required
    def marcar_incidencia_comunicada():
        """Marca o desmarca una incidencia como comunicada"""
        import db
        from models import IncidenciaAldipod
        data = request.get_json(silent=True) or {}
        incidencia_id = data.get('id')
        estado = data.get('comunicada')
        if incidencia_id is None or estado is None:
            return jsonify({"ok": False, "error": "Parámetros inválidos"}), 400
        incidencia = db.session.query(IncidenciaAldipod).filter_by(id=incidencia_id).first()
        if not incidencia:
            return jsonify({"ok": False, "error": "Incidencia no encontrada"}), 404
        incidencia.comunicada = bool(estado)
        db.session.commit()
        return jsonify({"ok": True})
    
    @app.route('/incidencia_aldipod/actualizar_observaciones', methods=['POST'])
    @login_required
    def actualizar_observaciones_incidencia():
        """Actualiza las observaciones de una incidencia por referencia"""
        import db
        from models import IncidenciaAldipod
        data = request.get_json(silent=True) or {}
        referencia = data.get('referencia')
        observaciones = data.get('observaciones')
        
        if referencia is None:
            return jsonify({"ok": False, "error": "Parámetro 'referencia' requerido"}), 400
        
        # Normalizar observaciones: None, '', o 'None' -> None
        if observaciones is None:
            obs_final = None
        elif isinstance(observaciones, str):
            obs_clean = observaciones.strip()
            if not obs_clean or obs_clean.lower() == 'none':
                obs_final = None
            else:
                obs_final = obs_clean
        else:
            obs_final = None
        
        # Buscar la incidencia más reciente con esa referencia
        incidencia = db.session.query(IncidenciaAldipod).filter_by(referencia=referencia).order_by(IncidenciaAldipod.fecha.desc()).first()
        
        if not incidencia:
            return jsonify({"ok": False, "error": "Incidencia no encontrada"}), 404
        
        print(f"DEBUG: Actualizando observaciones para referencia {referencia}: {repr(obs_final)}")
        incidencia.observaciones = obs_final
        db.session.commit()
        return jsonify({"ok": True, "mensaje": "Observaciones actualizadas correctamente"})

    @app.route('/aldipod/descargar_albaranes_simoes')
    @login_required
    def descargar_albaranes_simoes():
        """Genera y descarga un PDF único con todos los alb_clientes del cliente Simoes.
        Acepta:
        - fecha=YYYY-MM-DD (compatibilidad)
        - o rango: desde=YYYY-MM-DD&hasta=YYYY-MM-DD
        """
        import db
        from models import IncidenciaAldipod
        import fitz
        import paramiko

        fecha_str = request.args.get('fecha')
        desde_str = request.args.get('desde')
        hasta_str = request.args.get('hasta')

        if fecha_str:
            try:
                fecha = datetime.strptime(fecha_str, '%Y-%m-%d')
            except ValueError:
                return "Formato de fecha inválido. Use YYYY-MM-DD", 400
            desde = datetime(fecha.year, fecha.month, fecha.day, 0, 0, 0)
            hasta = datetime(fecha.year, fecha.month, fecha.day, 23, 59, 59)
        elif desde_str and hasta_str:
            try:
                desde = datetime.strptime(desde_str, '%Y-%m-%d')
                hasta = datetime.strptime(hasta_str, '%Y-%m-%d')
            except ValueError:
                return "Formato de rango inválido. Use YYYY-MM-DD", 400
            # Normalizar extremos del día
            desde = datetime(desde.year, desde.month, desde.day, 0, 0, 0)
            hasta = datetime(hasta.year, hasta.month, hasta.day, 23, 59, 59)
            fecha_str = f"{desde_str}_a_{hasta_str}"
        else:
            return "Falta parámetro fecha o rango desde/hasta", 400

        incidencias = db.session.query(IncidenciaAldipod).filter(
            IncidenciaAldipod.fecha >= desde,
            IncidenciaAldipod.fecha <= hasta,
            IncidenciaAldipod.tipo_documento == 'alb_clientes',
            IncidenciaAldipod.comunicada == False,
            IncidenciaAldipod.cliente.ilike('%simoes%')
        ).order_by(IncidenciaAldipod.fecha.asc()).all()

        if not incidencias:
            return "No hay albaranes para ese rango.", 404

        sftp_host = 'home613353667.1and1-data.host'
        sftp_user = 'u83991941-tsb'
        sftp_pass = 'tsb010Tx.MX'
        sftp_port = 22

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(sftp_host, port=sftp_port, username=sftp_user, password=sftp_pass, timeout=20)
            # Mantener viva la conexión y limitar bloqueos
            try:
                transport = ssh.get_transport()
                if transport:
                    transport.set_keepalive(10)
                    if hasattr(transport, 'sock') and transport.sock:
                        transport.sock.settimeout(15)
            except Exception:
                pass
            sftp = ssh.open_sftp()
        except Exception as e:
            return f"Error conectando a SFTP: {e}", 500

        merged_pdf = fitz.open()
        descargados = 0
        max_archivos = 200  # salvaguarda número de ficheros
        max_total_mb = 200   # límite de datos descargados
        total_descargado = 0
        import time
        inicio = time.time()
        presupuesto_seg = 45  # cortar antes del timeout del worker
        try:
            for idx, inc in enumerate(incidencias):
                if idx >= max_archivos:
                    break
                # Presupuesto de tiempo
                if time.time() - inicio > presupuesto_seg:
                    break
                enlace = inc.enlace_imagen or ''
                try:
                    m = re.match(r'sftp://[^/]+/(.+)$', enlace or '')
                    if not m:
                        # intentar construir ruta a partir de nombre archivo si viene sin enlace
                        # rutas candidatas por convención
                        posibles = []
                    else:
                        ruta_relativa = m.group(1)
                        posibles = [
                            ruta_relativa,
                            f"/{ruta_relativa}",
                        ]
                        # Si apunta a BACKUP, probar también directorio operativo
                        if ruta_relativa.startswith('ALDIPOD_BACKUP/'):
                            sin_backup = ruta_relativa.replace('ALDIPOD_BACKUP/', 'ALDIPOD/', 1)
                            posibles.append(sin_backup)
                            posibles.append(f"/{sin_backup}")

                    file_bytes = None
                    last_err = None
                    for ruta in posibles:
                        try:
                            # comprobación rápida
                            try:
                                sftp.stat(ruta)
                            except Exception:
                                pass
                            with sftp.open(ruta, 'rb') as f:
                                # Leer en chunks con límites para evitar bloqueos/OOM
                                try:
                                    if hasattr(f, 'prefetch'):
                                        f.prefetch()
                                except Exception:
                                    pass
                                chunk = f.read(64 * 1024)
                                buf = io.BytesIO()
                                file_size_limit = 25 * 1024 * 1024  # 25MB por archivo
                                leidos = 0
                                while chunk:
                                    buf.write(chunk)
                                    leidos += len(chunk)
                                    total_descargado += len(chunk)
                                    if leidos > file_size_limit:
                                        buf = None
                                        break
                                    if (total_descargado / (1024*1024)) > max_total_mb:
                                        break
                                    if time.time() - inicio > presupuesto_seg:
                                        break
                                    chunk = f.read(256 * 1024)
                                if buf is None:
                                    raise RuntimeError('archivo_supera_limite')
                                file_bytes = buf.getvalue()
                                break
                        except Exception as e_ruta:
                            last_err = e_ruta
                            continue
                    if file_bytes is None:
                        continue
                        # Leer en chunks con límites para evitar bloqueos/OOM
                        # Algunos servidores mejoran con prefetch
                        try:
                            if hasattr(f, 'prefetch'):
                                f.prefetch()
                        except Exception:
                            pass
                        chunk = f.read(64 * 1024)
                        buf = io.BytesIO()
                        file_size_limit = 25 * 1024 * 1024  # 25MB por archivo
                        leidos = 0
                        while chunk:
                            buf.write(chunk)
                            leidos += len(chunk)
                            total_descargado += len(chunk)
                            if leidos > file_size_limit:
                                # archivo demasiado grande, saltar
                                buf = None
                                break
                            if (total_descargado / (1024*1024)) > max_total_mb:
                                break
                            # Chequeo de tiempo por vuelta
                            if time.time() - inicio > presupuesto_seg:
                                break
                            chunk = f.read(256 * 1024)
                        if buf is None:
                            continue
                        if (total_descargado / (1024*1024)) > max_total_mb:
                            break
                        file_bytes = buf.getvalue()
                    try:
                        src = fitz.open(stream=file_bytes, filetype='pdf')
                    except Exception:
                        # Si no es PDF, abrir como imagen en un PDF temporal
                        src = fitz.open(stream=file_bytes, filetype='jpeg')
                        img_rect = src[0].rect
                        tmp_doc = fitz.open()
                        page = tmp_doc.new_page(width=img_rect.width, height=img_rect.height)
                        page.insert_image(img_rect, stream=file_bytes)
                        src.close()
                        src = tmp_doc

                    # Convertir a escala de grises y comprimir por página para reducir tamaño.
                    # Si falla por cualquier motivo, insertar el PDF original como fallback.
                    converted = False
                    try:
                        Matrix = fitz.Matrix
                        scale = 1.5  # ~108 dpi -> 72*1.5 = 108 dpi
                        for p in src:
                            pix = p.get_pixmap(matrix=Matrix(scale, scale), colorspace=fitz.csGRAY, alpha=False)
                            img_bytes = pix.tobytes("jpeg", quality=70)
                            rect = fitz.Rect(0, 0, pix.width, pix.height)
                            out_page = merged_pdf.new_page(width=rect.width, height=rect.height)
                            out_page.insert_image(rect, stream=img_bytes)
                        converted = True
                    except Exception:
                        try:
                            merged_pdf.insert_pdf(src)
                        except Exception:
                            pass
                    finally:
                        src.close()
                    descargados += 1
                except Exception:
                    continue
        finally:
            try:
                sftp.close()
            except Exception:
                pass
            try:
                ssh.close()
            except Exception:
                pass

        if descargados == 0:
            merged_pdf.close()
            return "No se pudieron descargar/abrir los archivos.", 404

        out_bytes = io.BytesIO()
        merged_pdf.save(out_bytes)
        merged_pdf.close()
        out_bytes.seek(0)
        filename = f"albaranes_simoes_{fecha_str}.pdf"
        return send_file(out_bytes, as_attachment=True, download_name=filename, mimetype='application/pdf')

    @app.route('/aldipod/marcar_albaranes_simoes_comunicados', methods=['POST'])
    @login_required
    def marcar_albaranes_simoes_comunicados():
        import db
        from models import IncidenciaAldipod
        data = request.get_json(silent=True) or {}
        fecha_str = data.get('fecha')
        desde_str = data.get('desde')
        hasta_str = data.get('hasta')

        if fecha_str:
            try:
                fecha = datetime.strptime(fecha_str, '%Y-%m-%d')
            except ValueError:
                return jsonify(ok=False, error='Formato de fecha inválido'), 400
            desde = datetime(fecha.year, fecha.month, fecha.day, 0, 0, 0)
            hasta = datetime(fecha.year, fecha.month, fecha.day, 23, 59, 59)
        elif desde_str and hasta_str:
            try:
                desde = datetime.strptime(desde_str, '%Y-%m-%d')
                hasta = datetime.strptime(hasta_str, '%Y-%m-%d')
            except ValueError:
                return jsonify(ok=False, error='Formato de rango inválido'), 400
            desde = datetime(desde.year, desde.month, desde.day, 0, 0, 0)
            hasta = datetime(hasta.year, hasta.month, hasta.day, 23, 59, 59)
        else:
            return jsonify(ok=False, error='Falta fecha o rango'), 400

        incidencias = db.session.query(IncidenciaAldipod).filter(
            IncidenciaAldipod.fecha >= desde,
            IncidenciaAldipod.fecha <= hasta,
            IncidenciaAldipod.tipo_documento == 'alb_clientes',
            IncidenciaAldipod.cliente.ilike('%simoes%')
        ).all()
        for inc in incidencias:
            inc.comunicada = True
        db.session.commit()
        return jsonify(ok=True, actualizados=len(incidencias))
    
    @app.route('/descargar_imagen/<referencia>')
    @login_required
    def descargar_imagen_incidencia(referencia):
        """Descarga una imagen de incidencia desde FTP usando la referencia"""
        import db
        from models import IncidenciaAldipod
        from flask import send_file
        import tempfile
        import os
        from ftplib import FTP
        
        incidencia = db.session.query(IncidenciaAldipod).filter_by(referencia=referencia).first()
        if not incidencia:
            return "Incidencia no encontrada", 404
        
        try:
            # Parsear URL SFTP/FTP
            enlace = incidencia.enlace_imagen
            print(f"DEBUG: Enlace de imagen: {enlace}")  # Debug
            
            if enlace.startswith('local://'):
                # Manejar copias locales en VPS
                ruta_relativa = enlace.replace('local://', '', 1).lstrip('/\\')
                backup_root = obtener_backup_local_root()
                ruta_absoluta = os.path.abspath(os.path.join(backup_root, ruta_relativa))
                if os.path.commonpath([backup_root, ruta_absoluta]) != backup_root:
                    return "Ruta local no válida", 400
                if not os.path.exists(ruta_absoluta):
                    return f"Archivo local no encontrado: {ruta_relativa}", 404

                filename = os.path.basename(ruta_absoluta)
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=f'_{filename}')
                with open(ruta_absoluta, 'rb') as f_src, open(temp_file.name, 'wb') as f_dst:
                    f_dst.write(f_src.read())

            elif enlace.startswith('sftp://'):
                # Manejar enlaces SFTP
                # Extraer componentes del URL SFTP: sftp://user@host/path/file
                url_parts = enlace.replace('sftp://', '').split('/')
                user_host = url_parts[0]
                if '@' in user_host:
                    user, host = user_host.split('@')
                else:
                    user, host = '', user_host
                file_path = '/'.join(url_parts[1:])
                filename = url_parts[-1]
                
                print(f"DEBUG: SFTP Host: {host}, User: {user}, File path: {file_path}, Filename: {filename}")  # Debug
                
                # Conectar por SFTP con helper robusto (IPv4 + socket + reintentos)
                ssh, sftp, ultimo_error_conexion = conectar_sftp_backup(max_intentos=4)

                if sftp:
                    # Verificar si el archivo existe
                    try:
                        file_stat = sftp.stat(file_path)
                        print(f"DEBUG: Archivo encontrado, tamaño: {file_stat.st_size} bytes")  # Debug
                    except FileNotFoundError:
                        sftp.close()
                        ssh.close()
                        return f"Archivo no encontrado en SFTP: {file_path}", 404
                    
                    # Crear archivo temporal
                    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=f'_{filename}')
                    
                    # Descargar archivo
                    sftp.get(file_path, temp_file.name)
                    
                    sftp.close()
                    ssh.close()
                else:
                    # Fallback: si SFTP cae (banner reset, timeout...), intentar por FTP principal.
                    print(f"WARNING: SFTP no disponible ({ultimo_error_conexion}). Intentando fallback FTP.")
                    from .funciones_scanner import cargar_configuracion_ftp
                    ftp_config = cargar_configuracion_ftp()
                    if not ftp_config:
                        return f"No se pudo conectar al SFTP tras varios intentos: {str(ultimo_error_conexion)}", 500

                    ftp = None
                    ultimo_error_login_ftp = None
                    # Intentar FTP explícito y, si falla, FTPS explícito (TLS)
                    for usar_tls in (False, True):
                        try:
                            if usar_tls:
                                from ftplib import FTP_TLS
                                ftp = FTP_TLS()
                            else:
                                ftp = FTP()
                            ftp.connect(ftp_config.get('host', ''), ftp_config.get('port', 21), timeout=15)
                            ftp.login(ftp_config.get('user', ''), ftp_config.get('password', ''))
                            if usar_tls:
                                ftp.prot_p()
                            break
                        except Exception as ftp_login_err:
                            ultimo_error_login_ftp = ftp_login_err
                            try:
                                if ftp:
                                    ftp.quit()
                            except Exception:
                                pass
                            ftp = None

                    if not ftp:
                        return (
                            f"No se pudo conectar al SFTP tras varios intentos: {str(ultimo_error_conexion)}. "
                            f"Fallback FTP/FTPS falló: {str(ultimo_error_login_ftp)}",
                            500
                        )

                    # Rutas candidatas en FTP para el mismo fichero.
                    posibles_rutas = []
                    if file_path:
                        raw_path = file_path.lstrip('/')
                        posibles_rutas.append(raw_path)
                        if raw_path.startswith('ALDIPOD_BACKUP/'):
                            posibles_rutas.append(raw_path.replace('ALDIPOD_BACKUP/', 'ALDIPOD/', 1))

                    # Ruta por tipo de documento como respaldo final
                    tipo_doc = (incidencia.tipo_documento or '').strip()
                    if tipo_doc == 'alb_clientes':
                        posibles_rutas.append(f"ALDIPOD/CLIENTES/{filename}")
                    elif tipo_doc == 'POD':
                        posibles_rutas.append(f"ALDIPOD/POD/{filename}")
                    else:
                        directorio = (ftp_config.get('directory') or '').strip('/')
                        if directorio:
                            posibles_rutas.append(f"{directorio}/{filename}")
                        posibles_rutas.append(filename)

                    # Quitar duplicados conservando orden
                    rutas_unicas = []
                    for ruta in posibles_rutas:
                        if ruta and ruta not in rutas_unicas:
                            rutas_unicas.append(ruta)

                    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=f'_{filename}')
                    ruta_ok = None
                    ultimo_error_ftp = None
                    for ruta in rutas_unicas:
                        try:
                            # Estrategia 1: ruta completa
                            try:
                                ftp.size(ruta)
                            except Exception:
                                pass
                            with open(temp_file.name, 'wb') as f:
                                ftp.retrbinary(f'RETR {ruta}', f.write)
                            ruta_ok = ruta
                            break
                        except Exception as ftp_err:
                            # Estrategia 2: cambiar a carpeta y descargar por nombre de fichero
                            try:
                                dir_ruta, nombre_ruta = ruta.rsplit('/', 1) if '/' in ruta else ('', ruta)
                                cwd_original = ftp.pwd()
                                if dir_ruta:
                                    ftp.cwd('/')
                                    for segmento in [s for s in dir_ruta.split('/') if s]:
                                        ftp.cwd(segmento)
                                with open(temp_file.name, 'wb') as f:
                                    ftp.retrbinary(f'RETR {nombre_ruta}', f.write)
                                ruta_ok = ruta
                                try:
                                    ftp.cwd(cwd_original)
                                except Exception:
                                    pass
                                break
                            except Exception as ftp_err_2:
                                ultimo_error_ftp = ftp_err_2
                                continue

                    ftp.quit()

                    if not ruta_ok:
                        try:
                            os.unlink(temp_file.name)
                        except Exception:
                            pass
                        return (
                            f"No se pudo descargar el archivo por SFTP ni por FTP. "
                            f"SFTP: {str(ultimo_error_conexion)} | FTP: {str(ultimo_error_ftp)}",
                            500
                        )
                    print(f"DEBUG: Descarga por FTP fallback exitosa en ruta: {ruta_ok}")
                
            elif enlace.startswith('ftp://'):
                # Manejar enlaces FTP (compatibilidad hacia atrás)
                # Extraer componentes del URL FTP
                url_parts = enlace.replace('ftp://', '').split('/')
                host = url_parts[0]
                file_path = '/'.join(url_parts[1:])
                filename = url_parts[-1]
                
                print(f"DEBUG: FTP Host: {host}, File path: {file_path}, Filename: {filename}")  # Debug
                
                # Cargar configuración FTP
                from .funciones_scanner import cargar_configuracion_ftp
                config = cargar_configuracion_ftp()
                if not config:
                    return "Configuración FTP no encontrada", 500
                
                print(f"DEBUG: Config FTP: {config}")  # Debug
                
                # Conectar a FTP
                try:
                    ftp = FTP(host)
                    ftp.login(config.get('user', ''), config.get('password', ''))
                    print("DEBUG: Conectado a FTP exitosamente")  # Debug
                except Exception as conn_err:
                    return f"No se pudo conectar al FTP ({host}). Posible bloqueo de red/puerto o credenciales incorrectas: {str(conn_err)}", 500
                
                # Verificar si el archivo existe
                try:
                    file_size = ftp.size(file_path)
                    print(f"DEBUG: Archivo encontrado, tamaño: {file_size} bytes")  # Debug
                except Exception as size_err:
                    print(f"DEBUG: No se pudo obtener tamaño del archivo: {file_path} -> {size_err}")  # Debug
                    ftp.quit()
                    return f"Archivo no encontrado en FTP: {file_path}", 404
                
                # Crear archivo temporal
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=f'_{filename}')
                
                # Descargar archivo
                with open(temp_file.name, 'wb') as f:
                    ftp.retrbinary(f'RETR {file_path}', f.write)
                
                ftp.quit()
            else:
                return f"Enlace no válido: {enlace}", 400
            
            # Verificar que el archivo se descargó correctamente
            if os.path.getsize(temp_file.name) == 0:
                os.unlink(temp_file.name)
                return "Archivo descargado está vacío", 500
            
            print(f"DEBUG: Archivo descargado exitosamente: {temp_file.name}")  # Debug
            
            # Enviar archivo
            # Setear mimetype según la extensión
            mimetype = 'application/pdf' if filename.lower().endswith('.pdf') else 'image/jpeg'
            response = send_file(
                temp_file.name,
                as_attachment=True,
                download_name=filename,
                mimetype=mimetype
            )
            
            # Limpiar archivo temporal después de enviar
            try:
                os.unlink(temp_file.name)
            except:
                pass
            
            return response
            
        except Exception as e:
            print(f"DEBUG: Error en descarga: {str(e)}")  # Debug
            return f"Error al descargar imagen: {str(e)}", 500
    
    @app.route('/test_camera')
    @login_required
    def test_camera():
        """Página de prueba para verificar el acceso a la cámara"""
        return render_template('test_camera.html')
    
    @app.route('/test_ftp')
    @login_required
    def test_ftp():
        """Prueba la conectividad FTP y SFTP"""
        from .funciones_scanner import cargar_configuracion_ftp
        from ftplib import FTP
        
        results = {}
        
        # Test FTP original
        try:
            config = cargar_configuracion_ftp()
            if not config:
                results['ftp'] = {'success': False, 'error': 'Configuración FTP no encontrada'}
            else:
                ftp = FTP(config.get('host', ''))
                ftp.login(config.get('user', ''), config.get('password', ''))
                
                # Listar directorio backup
                backup_files = []
                try:
                    ftp.cwd('/ALDIPOD/BACKUP')
                    backup_files = ftp.nlst()
                except:
                    pass
                
                ftp.quit()
                
                results['ftp'] = {
                    'success': True, 
                    'message': 'Conexión FTP exitosa',
                    'host': config.get('host', ''),
                    'backup_files': backup_files[:10]
                }
                
        except Exception as e:
            results['ftp'] = {'success': False, 'error': str(e)}
        
        # Test SFTP backup
        try:
            import paramiko
            
            sftp_host = 'home613353667.1and1-data.host'
            sftp_user = 'u83991941-tsb'
            sftp_pass = 'tsb010Tx.MX'
            sftp_port = 22
            sftp_dir = 'ALDIPOD_BACKUP'
            
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(sftp_host, port=sftp_port, username=sftp_user, password=sftp_pass, timeout=30)
            
            sftp = ssh.open_sftp()
            
            # Listar archivos en directorio backup
            backup_files = []
            try:
                backup_files = sftp.listdir(sftp_dir)
            except FileNotFoundError:
                backup_files = []
            
            sftp.close()
            ssh.close()
            
            results['sftp'] = {
                'success': True,
                'message': 'Conexión SFTP exitosa',
                'host': sftp_host,
                'backup_files': backup_files[:10]
            }
            
        except Exception as e:
            results['sftp'] = {'success': False, 'error': str(e)}
        
        return jsonify(results)
    
    @app.route('/validar_codigo', methods=['POST'])
    @login_required
    def validar_codigo():
        """Valida el código de barras escaneado"""
        data = request.get_json()
        codigo = data.get('codigo', '')
        
        if validar_codigo_barras(codigo):
            return jsonify({
                'success': True,
                'mensaje': f'Código válido: {codigo}'
            })
        else:
            return jsonify({
                'success': False,
                'mensaje': 'Código de barras inválido'
            })
    
    @app.route('/subir_imagen_scanner', methods=['POST'])
    @login_required
    def subir_imagen_scanner():
        """Recibe una o varias imágenes y el código, genera un PDF si hay varias y sube."""
        from .funciones_scanner import crear_pdf_temporal, generar_nombre_pdf
        data = request.get_json()
        imagen_data = data.get('imagen')  # string base64 (compat)
        imagenes = data.get('imagenes')   # lista de strings base64
        codigo_barras = data.get('codigo', '')
        cliente_id = data.get('cliente_id', None)
        tipo_registro = data.get('tipo_registro', 'INCIDENCIA')
        medidas = data.get('medidas', None)  # Para compatibilidad con flujo anterior
        medidas_por_foto = data.get('medidas_por_foto', None)  # Nuevo flujo con medidas por foto
        # Obtener observaciones y normalizar: None, '', o 'None' (string) -> None
        observaciones_raw = data.get('observaciones')
        if observaciones_raw is None:
            observaciones = None
        elif isinstance(observaciones_raw, str):
            observaciones = observaciones_raw.strip()
            # Si es string vacío o la palabra 'None', convertir a None
            if not observaciones or observaciones.lower() == 'none':
                observaciones = None
        else:
            observaciones = None

        if (not imagen_data and not imagenes) or not codigo_barras:
            return jsonify({'success': False,'mensaje': 'Faltan datos: imagen(es) o código de barras'})

        try:
            usuario = current_user.username if current_user.is_authenticated else "Anónimo"
            print(f"DEBUG: Usuario: {usuario}")
            print(f"DEBUG: Tipo registro: {tipo_registro}")
            print(f"DEBUG: Medidas recibidas: {medidas}")
            print(f"DEBUG: Medidas por foto recibidas: {medidas_por_foto}")
            print(f"DEBUG: Observaciones recibidas: '{observaciones}' (tipo: {type(observaciones)}, longitud: {len(observaciones) if observaciones else 0})")

            # Normalizar a lista siempre
            imagenes_norm = imagenes if (imagenes and isinstance(imagenes, list)) else ([imagen_data] if imagen_data else [])
            # Generar PDF siempre
            nombre_pdf = generar_nombre_pdf(codigo_barras)
            
            # Usar medidas_por_foto si está disponible, sino usar medidas (compatibilidad)
            medidas_a_usar = medidas_por_foto if medidas_por_foto else medidas
            ok, ruta_pdf, err = crear_pdf_temporal(imagenes_norm, nombre_pdf, medidas_a_usar, tipo_registro)
            if not ok:
                return jsonify({'success': False, 'mensaje': f'Error creando PDF: {err}'})

            # Subir PDF
            success, mensaje, enlace_generado = subir_archivo_ftp(ruta_pdf, nombre_pdf, cliente_id, tipo_registro)
            if success:
                # Registrar incidencia en la base de datos
                registro_ok, registro_msg, incidencia_id = registrar_incidencia(
                    usuario, cliente_id, codigo_barras, nombre_pdf, tipo_registro, medidas_a_usar, observaciones, enlace_generado
                )
                if not registro_ok:
                    # Si falla el registro, reportar el error
                    print(f"ERROR CRÍTICO: Archivo subido pero registro en BD falló: {registro_msg}")
                    # Limpiar archivo temporal
                    try:
                        os.remove(ruta_pdf)
                    except:
                        pass
                    return jsonify({
                        'success': False, 
                        'mensaje': f'Archivo subido pero error al registrar en BD: {registro_msg}'
                    })
                else:
                    print(f"DEBUG: Registro exitoso - {registro_msg}")
            try:
                os.remove(ruta_pdf)
            except:
                pass
            return jsonify({'success': success, 'mensaje': mensaje})
        except Exception as e:
            return jsonify({'success': False,'mensaje': f'Error al procesar la imagen: {str(e)}'})

