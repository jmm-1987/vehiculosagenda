"""
Rutas para el scanner de códigos de barras y subida de imágenes a FTP
"""
from flask import render_template, request, jsonify
from flask_login import login_required, current_user
from .funciones_scanner import (
    subir_archivo_ftp, 
    validar_codigo_barras, 
    limpiar_nombre_archivo,
    guardar_imagen_temporal,
    limpiar_archivos_temporales,
    registrar_incidencia
)
import os

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
            
            if enlace.startswith('sftp://'):
                # Manejar enlaces SFTP
                import paramiko
                
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
                
                # Configuración SFTP de backup
                sftp_config = {
                    'host': 'home613353667.1and1-data.host',
                    'user': 'u83991941-tsb',
                    'password': 'tsb010Tx.MX',
                    'port': 22
                }
                
                # Conectar por SFTP
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(sftp_config['host'], port=sftp_config['port'], 
                           username=sftp_config['user'], password=sftp_config['password'])
                
                sftp = ssh.open_sftp()
                
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

        if (not imagen_data and not imagenes) or not codigo_barras:
            return jsonify({'success': False,'mensaje': 'Faltan datos: imagen(es) o código de barras'})

        try:
            usuario = current_user.username if current_user.is_authenticated else "Anónimo"
            print(f"DEBUG: Usuario: {usuario}")
            print(f"DEBUG: Tipo registro: {tipo_registro}")
            print(f"DEBUG: Medidas recibidas: {medidas}")
            print(f"DEBUG: Medidas por foto recibidas: {medidas_por_foto}")

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
            success, mensaje = subir_archivo_ftp(ruta_pdf, nombre_pdf, cliente_id, tipo_registro)
            if success:
                registrar_incidencia(usuario, cliente_id, codigo_barras, nombre_pdf, tipo_registro, medidas_a_usar)
            try:
                os.remove(ruta_pdf)
            except:
                pass
            return jsonify({'success': success, 'mensaje': mensaje})
        except Exception as e:
            return jsonify({'success': False,'mensaje': f'Error al procesar la imagen: {str(e)}'})

