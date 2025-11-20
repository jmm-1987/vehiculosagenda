"""
Rutas para el procesamiento del formulario de RRHH desde web externa.
"""

from flask import request, jsonify
from flask_cors import cross_origin
from rrhh_mailer import enviar_formulario_rrhh, ConfiguracionSMTPError


def register_rrhh_routes(app):
    """Registra las rutas para el formulario de RRHH."""
    
    @app.route('/api/rrhh/formulario', methods=['POST', 'OPTIONS'])
    @cross_origin()
    def procesar_formulario_rrhh():
        """
        Endpoint para recibir y procesar el formulario de RRHH desde una web externa.
        
        Acepta datos del formulario y un archivo PDF opcional del currículum.
        Envía un correo con los datos a jmurillo@alditraex.es.
        
        Formato esperado:
        - Content-Type: multipart/form-data
        - Campos: nombre_completo, correo_electronico, telefono, area_interes, presentacion
        - Archivo: curriculum_pdf (opcional)
        
        Respuesta JSON:
        - success: bool
        - message: str
        """
        try:
            # Validar que sea una petición POST
            if request.method != 'POST':
                return jsonify({
                    'success': False,
                    'message': 'Método no permitido. Use POST.'
                }), 405
            
            # Obtener datos del formulario
            datos_formulario = {
                'nombre_completo': request.form.get('nombre_completo', '').strip(),
                'correo_electronico': request.form.get('correo_electronico', '').strip(),
                'telefono': request.form.get('telefono', '').strip(),
                'area_interes': request.form.get('area_interes', '').strip(),
                'presentacion': request.form.get('presentacion', '').strip(),
            }
            
            # Obtener archivo PDF si existe
            curriculum_pdf = None
            if 'curriculum_pdf' in request.files:
                archivo = request.files['curriculum_pdf']
                if archivo and archivo.filename:
                    # Validar que sea PDF
                    if not archivo.filename.lower().endswith('.pdf'):
                        return jsonify({
                            'success': False,
                            'message': 'El archivo del currículum debe ser un PDF (.pdf)'
                        }), 400
                    curriculum_pdf = archivo
            
            # Enviar correo
            enviar_formulario_rrhh(datos_formulario, curriculum_pdf)
            
            return jsonify({
                'success': True,
                'message': 'Formulario recibido y correo enviado correctamente.'
            }), 200
            
        except ConfiguracionSMTPError as e:
            return jsonify({
                'success': False,
                'message': f'Error de configuración del servidor de correo: {str(e)}'
            }), 500
            
        except ValueError as e:
            return jsonify({
                'success': False,
                'message': f'Datos del formulario incompletos: {str(e)}'
            }), 400
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error al procesar el formulario: {str(e)}'
            }), 500

