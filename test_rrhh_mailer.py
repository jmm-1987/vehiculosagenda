"""
Script de prueba para verificar el envío de correos del formulario de RRHH.
"""

from rrhh_mailer import enviar_formulario_rrhh, ConfiguracionSMTPError

# Datos de prueba basados en el formulario de la imagen
datos_prueba = {
    "nombre_completo": "Juan Pérez García",
    "correo_electronico": "juan.perez@ejemplo.com",
    "telefono": "654654654",
    "area_interes": "Gestión de tráfico",
    "presentacion": "Esta es una prueba del sistema de envío de formularios de RRHH."
}

if __name__ == "__main__":
    print("=" * 60)
    print("PRUEBA DE ENVÍO DE CORREO - FORMULARIO RRHH")
    print("=" * 60)
    print(f"\nEnviando correo desde: rrhh@alditraex.es")
    print(f"Enviando correo hacia: jmurillo@alditraex.es")
    print(f"\nDatos del formulario:")
    for clave, valor in datos_prueba.items():
        print(f"  - {clave}: {valor}")
    print("\n" + "-" * 60)
    
    try:
        # Nota: Para puerto 465 (SSL), necesitamos use_ssl=True
        # Si prefieres usar TLS, cambia el puerto a 587
        enviar_formulario_rrhh(
            datos_prueba,
            curriculum_pdf=None,  # Sin adjunto para esta prueba
            smtp_config={
                "use_ssl": True,  # Puerto 465 requiere SSL
                "use_tls": False
            }
        )
        print("[OK] ¡Correo enviado correctamente!")
        print("\nPor favor, verifica la bandeja de entrada de jmurillo@alditraex.es")
        
    except ConfiguracionSMTPError as e:
        print(f"[ERROR] Error de configuracion SMTP: {e}")
    except Exception as e:
        print(f"[ERROR] Error al enviar el correo: {e}")
        import traceback
        print("\nDetalles del error:")
        traceback.print_exc()

