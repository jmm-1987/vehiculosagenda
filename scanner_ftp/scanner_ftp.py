"""
Rutas para el scanner de códigos de barras y subida de imágenes a FTP
"""
from flask import render_template, request, jsonify
from flask_login import login_required
from .funciones_scanner import (
    subir_archivo_ftp, 
    validar_codigo_barras, 
    limpiar_nombre_archivo,
    guardar_imagen_temporal,
    limpiar_archivos_temporales
)
import os

def register_scanner_ftp_routes(app):
    """Registra las rutas del scanner FTP"""
    
    @app.route('/scanner_clientes')

    def scanner_clientes():
        """Muestra la página con los 8 contenedores de clientes"""
        # Limpiar archivos temporales antiguos
        limpiar_archivos_temporales()
        return render_template('scanner_clientes.html')
    
    @app.route('/test_camera')

    def test_camera():
        """Página de prueba para verificar el acceso a la cámara"""
        return render_template('test_camera.html')
    
    @app.route('/validar_codigo', methods=['POST'])

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
            nombre_archivo = limpiar_nombre_archivo(codigo_barras)
            
            # Guardar imagen temporalmente
            ruta_temporal = guardar_imagen_temporal(imagen_data, nombre_archivo)
            
            # Subir al FTP
            success, mensaje = subir_archivo_ftp(ruta_temporal, nombre_archivo, cliente_id)
            
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

