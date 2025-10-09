"""
Funciones auxiliares para el scanner de códigos de barras y subida FTP
"""
import ftplib
import json
import os
from datetime import datetime

def cargar_configuracion_ftp():
    """Carga la configuración del FTP desde el archivo JSON"""
    try:
        with open('static/ftp_config.json', 'r') as f:
            config = json.load(f)
        # Usar la configuración "origen" del archivo existente
        if 'origen' in config:
            origen = config['origen']
            return {
                'host': origen.get('ftp', 'localhost'),
                'port': 21,
                'user': origen.get('username', ''),
                'password': origen.get('password', ''),
                'directory': origen.get('directory', 'scanner_images')
            }
        return config
    except Exception as e:
        print(f"Error al cargar configuración FTP: {e}")
        return None

def subir_archivo_ftp(archivo_local, nombre_remoto, cliente_id=None):
    """
    Sube un archivo al servidor FTP
    
    Args:
        archivo_local: ruta local del archivo
        nombre_remoto: nombre que tendrá el archivo en el servidor
        cliente_id: identificador del cliente (1-8)
    
    Returns:
        tuple: (success: bool, message: str)
    """
    config = cargar_configuracion_ftp()
    
    if not config:
        return False, "No se pudo cargar la configuración FTP"
    
    try:
        # Conectar al servidor FTP
        ftp = ftplib.FTP()
        ftp.connect(config.get('host', 'localhost'), config.get('port', 21))
        ftp.login(config.get('user', ''), config.get('password', ''))
        
        # Cambiar a directorio específico si existe en la config
        if 'directory' in config and config['directory']:
            try:
                ftp.cwd(config['directory'])
            except:
                # Si no existe el directorio, intentar crearlo
                ftp.mkd(config['directory'])
                ftp.cwd(config['directory'])
        
        # Si hay cliente_id, crear/acceder a subdirectorio del cliente
        if cliente_id:
            directorio_cliente = f'cliente_{cliente_id}'
            try:
                ftp.cwd(directorio_cliente)
            except:
                ftp.mkd(directorio_cliente)
                ftp.cwd(directorio_cliente)
        
        # Subir el archivo
        with open(archivo_local, 'rb') as file:
            ftp.storbinary(f'STOR {nombre_remoto}', file)
        
        ftp.quit()
        return True, f"Archivo {nombre_remoto} subido correctamente"
        
    except ftplib.all_errors as e:
        return False, f"Error FTP: {str(e)}"
    except Exception as e:
        return False, f"Error: {str(e)}"

def validar_codigo_barras(codigo):
    """
    Valida que el código de barras tenga un formato válido
    
    Args:
        codigo: string con el código de barras
    
    Returns:
        bool: True si es válido
    """
    if not codigo or len(codigo.strip()) == 0:
        return False
    
    # Puedes añadir más validaciones específicas aquí
    # Por ejemplo, longitud mínima, caracteres permitidos, etc.
    return len(codigo.strip()) >= 3

def limpiar_nombre_archivo(codigo_barras):
    """
    Limpia el código de barras para usarlo como nombre de archivo
    Elimina caracteres no permitidos en nombres de archivo
    
    Args:
        codigo_barras: string con el código de barras
    
    Returns:
        str: nombre de archivo limpio con extensión .jpg
    """
    # Caracteres no permitidos en nombres de archivo
    caracteres_invalidos = '<>:"/\\|?*'
    nombre_limpio = codigo_barras.strip()
    
    for char in caracteres_invalidos:
        nombre_limpio = nombre_limpio.replace(char, '_')
    
    # Añadir timestamp para evitar duplicados
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f"{nombre_limpio}_{timestamp}.jpg"

def guardar_imagen_temporal(imagen_data, nombre_archivo):
    """
    Guarda una imagen temporalmente en el servidor
    
    Args:
        imagen_data: datos de la imagen en base64
        nombre_archivo: nombre para guardar el archivo
    
    Returns:
        str: ruta del archivo guardado
    """
    import base64
    
    # Crear directorio temporal si no existe
    directorio_temp = 'static/temp_scanner'
    if not os.path.exists(directorio_temp):
        os.makedirs(directorio_temp)
    
    ruta_completa = os.path.join(directorio_temp, nombre_archivo)
    
    # Decodificar y guardar la imagen
    if 'base64,' in imagen_data:
        imagen_data = imagen_data.split('base64,')[1]
    
    with open(ruta_completa, 'wb') as f:
        f.write(base64.b64decode(imagen_data))
    
    return ruta_completa

def limpiar_archivos_temporales():
    """
    Limpia archivos temporales antiguos (más de 1 hora)
    """
    import time
    
    directorio_temp = 'static/temp_scanner'
    if not os.path.exists(directorio_temp):
        return
    
    ahora = time.time()
    hora_en_segundos = 3600
    
    for archivo in os.listdir(directorio_temp):
        ruta_archivo = os.path.join(directorio_temp, archivo)
        if os.path.isfile(ruta_archivo):
            tiempo_archivo = os.path.getmtime(ruta_archivo)
            if ahora - tiempo_archivo > hora_en_segundos:
                try:
                    os.remove(ruta_archivo)
                except:
                    pass

