"""
Funciones auxiliares para el scanner de códigos de barras y subida FTP
"""
import ftplib
import json
import os
from datetime import datetime, timezone, timedelta
import db
from models import IncidenciaAldipod

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
        destino_principal = None
        if 'directory' in config and config['directory']:
            destino_principal = config['directory']
            try:
                ftp.cwd(destino_principal)
            except:
                # Si no existe el directorio, intentar crearlo (y sus padres si hace falta)
                partes = destino_principal.split('/')
                ruta_acumulada = ''
                for p in partes:
                    if not p:
                        continue
                    ruta_acumulada = f"{ruta_acumulada}/{p}" if ruta_acumulada else p
                    try:
                        ftp.cwd(ruta_acumulada)
                    except:
                        ftp.mkd(ruta_acumulada)
                        ftp.cwd(ruta_acumulada)
        
        # Todos los clientes guardan en el mismo directorio, sin subcarpetas
        
        # Subir el archivo al destino principal
        with open(archivo_local, 'rb') as file:
            ftp.storbinary(f'STOR {nombre_remoto}', file)
        
        # Cerrar conexión FTP principal
        ftp.quit()
        
        # Adicional: subir copia a servidor SFTP de backup
        try:
            import paramiko
            import stat
            
            # Configuración del servidor SFTP de backup
            sftp_host = 'home613353667.1and1-data.host'
            sftp_user = 'u83991941-tsb'
            sftp_pass = 'tsb010Tx.MX'
            sftp_port = 22
            sftp_dir = 'ALDIPOD_BACKUP'
            
            print(f"DEBUG SFTP: Intentando conectar a {sftp_host}:{sftp_port} con usuario {sftp_user}")
            
            # Conectar por SFTP
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(sftp_host, port=sftp_port, username=sftp_user, password=sftp_pass, timeout=30)
            print("DEBUG SFTP: Conexión SSH exitosa")
            
            sftp = ssh.open_sftp()
            print("DEBUG SFTP: Conexión SFTP exitosa")
            
            # Crear directorio si no existe
            try:
                sftp.mkdir(sftp_dir)
                print(f"DEBUG SFTP: Directorio {sftp_dir} creado")
            except FileExistsError:
                print(f"DEBUG SFTP: Directorio {sftp_dir} ya existe")
            except OSError as mkdir_err:
                if "File exists" in str(mkdir_err) or "Failure" in str(mkdir_err):
                    print(f"DEBUG SFTP: Directorio {sftp_dir} ya existe (OSError)")
                else:
                    print(f"DEBUG SFTP: Error al crear directorio: {mkdir_err}")
            except Exception as mkdir_err:
                print(f"DEBUG SFTP: Error al crear directorio: {mkdir_err}")
            
            # Subir archivo
            remote_path = f"{sftp_dir}/{nombre_remoto}"
            print(f"DEBUG SFTP: Subiendo archivo a {remote_path}")
            sftp.put(archivo_local, remote_path)
            print(f"DEBUG SFTP: Archivo subido exitosamente")
            
            sftp.close()
            ssh.close()
            print("DEBUG SFTP: Conexiones cerradas correctamente")
            
        except ImportError:
            print("WARNING: paramiko no está instalado. No se puede subir backup SFTP.")
        except paramiko.AuthenticationException as auth_err:
            print(f"WARNING: Error de autenticación SFTP: {auth_err}")
        except paramiko.SSHException as ssh_err:
            print(f"WARNING: Error SSH/SFTP: {ssh_err}")
        except Exception as sftp_error:
            print(f"WARNING: Error al subir backup SFTP: {type(sftp_error).__name__}: {str(sftp_error)}")
            # No fallar la operación principal por error de backup
        
        return True, f"Archivo {nombre_remoto} subido correctamente (principal y SFTP backup)"
        
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

def limpiar_nombre_archivo(codigo_barras, cliente_id=None):
    """
    Limpia el código de barras para usarlo como nombre de archivo
    Elimina caracteres no permitidos en nombres de archivo
    
    Args:
        codigo_barras: string con el código de barras
        cliente_id: identificador del cliente (1-8)
    
    Returns:
        str: nombre de archivo limpio con extensión .jpg (solo el código de barras leído)
    """
    # Caracteres no permitidos en nombres de archivo
    caracteres_invalidos = '<>:"/\\|?*'
    nombre_limpio = codigo_barras.strip()
    
    for char in caracteres_invalidos:
        nombre_limpio = nombre_limpio.replace(char, '_')
    
    # Todos los clientes usan solo el código de barras sin timestamp
    return f"{nombre_limpio}.jpg"

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

def registrar_incidencia(usuario, cliente_id, referencia, nombre_archivo):
    """
    Registra una incidencia en la base de datos
    
    Args:
        usuario: nombre del usuario que sube la imagen
        cliente_id: identificador del cliente (1-8)
        referencia: código de barras escaneado
        nombre_archivo: nombre del archivo subido
    """
    # Mapeo de cliente_id a nombre de cliente
    clientes_map = {
        1: 'XPO Logistics',
        '1': 'XPO Logistics',
        2: 'Surpaq',
        '2': 'Surpaq',
        3: 'TSB',
        '3': 'TSB',
        4: 'Alditraex',
        '4': 'Alditraex',
        5: 'NTL',
        '5': 'NTL',
        6: 'Simoes',
        '6': 'Simoes',
        7: 'Essers',
        '7': 'Essers',
        8: 'BDtrans',
        '8': 'BDtrans'
    }
    
    nombre_cliente = clientes_map.get(cliente_id, f'Cliente {cliente_id}')
    
    # Construir enlace al servidor SFTP de backup (más confiable para descargas)
    sftp_host = 'home613353667.1and1-data.host'
    sftp_user = 'u83991941-tsb'
    sftp_dir = 'ALDIPOD_BACKUP'
    enlace = f"sftp://{sftp_user}@{sftp_host}/{sftp_dir}/{nombre_archivo}"
    tipo_documento = 'INCIDENCIA'
    
    try:
        # Crear fecha con zona horaria de España (UTC+2)
        now_utc = datetime.now(timezone.utc)
        now_spain = now_utc.astimezone(timezone(timedelta(hours=2)))
        
        incidencia = IncidenciaAldipod(
            fecha=now_spain,
            usuario=usuario,
            cliente=nombre_cliente,
            referencia=referencia,
            enlace_imagen=enlace,
            tipo_documento=tipo_documento
        )
        db.session.add(incidencia)
        db.session.commit()
    except Exception as e:
        print(f"Error al registrar incidencia: {e}")
        db.session.rollback()

