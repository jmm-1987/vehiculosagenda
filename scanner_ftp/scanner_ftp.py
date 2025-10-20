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
        
        # Obtener todas las incidencias ordenadas por fecha descendente
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
            # Parsear URL FTP
            enlace = incidencia.enlace_imagen
            print(f"DEBUG: Enlace de imagen: {enlace}")  # Debug
            
            if not enlace.startswith('ftp://'):
                return f"Enlace no válido: {enlace}", 400
            
            # Extraer componentes del URL FTP
            url_parts = enlace.replace('ftp://', '').split('/')
            host = url_parts[0]
            file_path = '/'.join(url_parts[1:])
            filename = url_parts[-1]
            
            print(f"DEBUG: Host: {host}, File path: {file_path}, Filename: {filename}")  # Debug
            
            # Cargar configuración FTP
            from .funciones_scanner import cargar_configuracion_ftp
            config = cargar_configuracion_ftp()
            if not config:
                return "Configuración FTP no encontrada", 500
            
            print(f"DEBUG: Config FTP: {config}")  # Debug
            
            # Conectar a FTP
            ftp = FTP(host)
            ftp.login(config.get('user', ''), config.get('password', ''))
            print("DEBUG: Conectado a FTP exitosamente")  # Debug
            
            # Verificar si el archivo existe
            try:
                file_size = ftp.size(file_path)
                print(f"DEBUG: Archivo encontrado, tamaño: {file_size} bytes")  # Debug
            except:
                print(f"DEBUG: No se pudo obtener tamaño del archivo: {file_path}")  # Debug
                ftp.quit()
                return f"Archivo no encontrado en FTP: {file_path}", 404
            
            # Crear archivo temporal
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=f'_{filename}')
            
            # Descargar archivo
            with open(temp_file.name, 'wb') as f:
                ftp.retrbinary(f'RETR {file_path}', f.write)
            
            ftp.quit()
            
            # Verificar que el archivo se descargó correctamente
            if os.path.getsize(temp_file.name) == 0:
                os.unlink(temp_file.name)
                return "Archivo descargado está vacío", 500
            
            print(f"DEBUG: Archivo descargado exitosamente: {temp_file.name}")  # Debug
            
            # Enviar archivo
            response = send_file(
                temp_file.name,
                as_attachment=True,
                download_name=filename,
                mimetype='image/jpeg'
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
        """Prueba la conectividad FTP"""
        from .funciones_scanner import cargar_configuracion_ftp
        from ftplib import FTP
        
        try:
            config = cargar_configuracion_ftp()
            if not config:
                return jsonify({'success': False, 'error': 'Configuración FTP no encontrada'})
            
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
            
            return jsonify({
                'success': True, 
                'message': 'Conexión FTP exitosa',
                'host': config.get('host', ''),
                'backup_files': backup_files[:10]  # Solo los primeros 10
            })
            
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})
    
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
        """Recibe la imagen y el código de barras, y sube al FTP"""
        data = request.get_json()
        imagen_data = data.get('imagen', '')
        codigo_barras = data.get('codigo', '')
        cliente_id = data.get('cliente_id', None)
        
        if not imagen_data or not codigo_barras:
            return jsonify({
                'success': False,
                'mensaje': 'Faltan datos: imagen o código de barras'
            })
        
        try:
            # Limpiar nombre de archivo
            nombre_archivo = limpiar_nombre_archivo(codigo_barras, cliente_id)
            
            # Guardar imagen temporalmente
            ruta_temporal = guardar_imagen_temporal(imagen_data, nombre_archivo)
            
            # Subir al FTP
            success, mensaje = subir_archivo_ftp(ruta_temporal, nombre_archivo, cliente_id)
            
            # Si la subida fue exitosa, registrar la incidencia
            if success:
                usuario = current_user.username if current_user.is_authenticated else "Anónimo"
                registrar_incidencia(usuario, cliente_id, codigo_barras, nombre_archivo)
            
            # Limpiar archivo temporal
            try:
                os.remove(ruta_temporal)
            except:
                pass
            
            return jsonify({
                'success': success,
                'mensaje': mensaje
            })
            
        except Exception as e:
            return jsonify({
                'success': False,
                'mensaje': f'Error al procesar la imagen: {str(e)}'
            })

