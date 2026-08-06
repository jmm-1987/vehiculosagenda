"""
Funciones auxiliares para el scanner de códigos de barras y subida FTP
"""
import ftplib
import json
import os
import random
import shutil
import socket
import string
import time
from datetime import datetime, timezone, timedelta
try:
    from zoneinfo import ZoneInfo
    ZONEINFO_AVAILABLE = True
except ImportError:
    try:
        import pytz
        ZONEINFO_AVAILABLE = False
        PYTZ_AVAILABLE = True
    except ImportError:
        ZONEINFO_AVAILABLE = False
        PYTZ_AVAILABLE = False
import db
from models import IncidenciaAldipod
from typing import List, Tuple
import paramiko

SFTP_BACKUP_HOST = 'home613353667.1and1-data.host'
SFTP_BACKUP_USER = 'u83991941-tsb'
SFTP_BACKUP_PASS = 'tsb010Tx.MX'
SFTP_BACKUP_PORT = 22
LOCAL_BACKUP_ROOT = '/var/lib/vehiculosagenda/aldipod_backup'


def conectar_sftp_backup(max_intentos=4):
    """
    Conecta al SFTP de backup forzando IPv4 y reintentando para evitar
    cortes intermitentes durante el banner SSH.
    """
    ultimo_error = None
    ips = []

    try:
        info = socket.getaddrinfo(
            SFTP_BACKUP_HOST,
            SFTP_BACKUP_PORT,
            family=socket.AF_INET,
            type=socket.SOCK_STREAM
        )
        for item in info:
            ip = item[4][0]
            if ip not in ips:
                ips.append(ip)
    except Exception:
        # Fallback: dejar que paramiko resuelva el host
        ips = [SFTP_BACKUP_HOST]

    for intento in range(1, max_intentos + 1):
        for destino in ips:
            ssh = None
            sock = None
            try:
                sock = socket.create_connection((destino, SFTP_BACKUP_PORT), timeout=12)
                sock.settimeout(25)

                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(
                    hostname=SFTP_BACKUP_HOST,
                    username=SFTP_BACKUP_USER,
                    password=SFTP_BACKUP_PASS,
                    sock=sock,
                    timeout=15,
                    banner_timeout=35,
                    auth_timeout=25,
                    look_for_keys=False,
                    allow_agent=False
                )
                transport = ssh.get_transport()
                if transport:
                    transport.set_keepalive(15)
                sftp = ssh.open_sftp()
                return ssh, sftp, None
            except Exception as e:
                ultimo_error = e
                try:
                    if ssh:
                        ssh.close()
                except Exception:
                    pass
                try:
                    if sock:
                        sock.close()
                except Exception:
                    pass
        if intento < max_intentos:
            time.sleep(1.2 * intento)

    return None, None, ultimo_error

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


def obtener_backup_local_root():
    """
    Ruta base de backup local fuera del proyecto.
    Fijada en código para evitar dependencia de variables de entorno.
    """
    return os.path.abspath(LOCAL_BACKUP_ROOT)


def guardar_copia_local_backup(archivo_local, nombre_remoto, tipo_documento):
    """
    Guarda una copia local en el VPS para no depender del backup SFTP.
    Retorna (ok, ruta_relativa_local, error)
    """
    try:
        fecha_hoy = datetime.now().strftime('%Y/%m/%d')
        if tipo_documento == 'POD':
            subdir = os.path.join('POD', fecha_hoy)
        elif tipo_documento == 'alb_clientes':
            subdir = os.path.join('CLIENTES', fecha_hoy)
        else:
            subdir = fecha_hoy

        backup_root = obtener_backup_local_root()
        directorio_destino = os.path.join(backup_root, subdir)
        os.makedirs(directorio_destino, exist_ok=True)
        destino = os.path.join(directorio_destino, nombre_remoto)
        shutil.copy2(archivo_local, destino)

        # Guardar ruta relativa al root de backups para mantenerla portable
        ruta_relativa = os.path.relpath(destino, start=backup_root).replace('\\', '/')
        return True, ruta_relativa, None
    except Exception as e:
        return False, None, e

def subir_archivo_ftp(archivo_local, nombre_remoto, cliente_id=None, tipo_documento="INCIDENCIA"):
    """
    Sube un archivo al servidor FTP
    
    Args:
        archivo_local: ruta local del archivo
        nombre_remoto: nombre que tendrá el archivo en el servidor
        cliente_id: identificador del cliente (1-8)
        tipo_documento: tipo de documento (INCIDENCIA, MEDIDAS, POD)
    
    Returns:
        tuple: (success: bool, message: str, enlace_imagen: str, nombre_local: str)
              nombre_local incluye sufijo aleatorio para la copia en el VPS;
              en Nereid se sube con nombre_remoto sin modificar.
    """
    config = cargar_configuracion_ftp()
    
    if not config:
        return False, "No se pudo cargar la configuración FTP", None, None
    
    try:
        # Conectar al servidor FTP
        ftp = ftplib.FTP()
        ftp.connect(config.get('host', 'localhost'), config.get('port', 21))
        ftp.login(config.get('user', ''), config.get('password', ''))
        
        ftp_remote_path = None
        backup_local_ok = False

        # Si es tipo POD, subir al directorio ALDIPOD/POD
        # Si es tipo alb_clientes, subir al directorio ALDIPOD/CLIENTES
        if tipo_documento == 'POD':
            try:
                # Cambiar al directorio ALDIPOD/POD
                try:
                    ftp.cwd('ALDIPOD')
                except:
                    ftp.mkd('ALDIPOD')
                    ftp.cwd('ALDIPOD')
                
                try:
                    ftp.cwd('POD')
                except:
                    ftp.mkd('POD')
                    ftp.cwd('POD')
                    
                print(f"DEBUG FTP: Directorio ALDIPOD/POD verificado/creado")
            except Exception as e:
                print(f"DEBUG FTP: Error al cambiar/crear directorio ALDIPOD/POD: {e}")
                # Intentar crear el directorio completo
                partes = ['ALDIPOD', 'POD']
                ruta_acumulada = ''
                for p in partes:
                    if not p:
                        continue
                    ruta_acumulada = f"{ruta_acumulada}/{p}" if ruta_acumulada else p
                    try:
                        # Intentar navegar
                        ftp.cwd(ruta_acumulada)
                    except:
                        # Si falla, intentar crear
                        try:
                            ftp.mkd(ruta_acumulada)
                            ftp.cwd(ruta_acumulada)
                        except:
                            pass
            
            # Subir al directorio ALDIPOD/POD
            with open(archivo_local, 'rb') as file:
                ftp.storbinary(f'STOR {nombre_remoto}', file)
            ftp_remote_path = f"ALDIPOD/POD/{nombre_remoto}"
            print(f"DEBUG FTP: Archivo subido al directorio ALDIPOD/POD")
        
        elif tipo_documento == 'alb_clientes':
            try:
                # Cambiar al directorio ALDIPOD/CLIENTES
                try:
                    ftp.cwd('ALDIPOD')
                except:
                    ftp.mkd('ALDIPOD')
                    ftp.cwd('ALDIPOD')
                
                try:
                    ftp.cwd('CLIENTES')
                except:
                    ftp.mkd('CLIENTES')
                    ftp.cwd('CLIENTES')
                    
                print(f"DEBUG FTP: Directorio ALDIPOD/CLIENTES verificado/creado")
            except Exception as e:
                print(f"DEBUG FTP: Error al cambiar/crear directorio ALDIPOD/CLIENTES: {e}")
                # Intentar crear el directorio completo
                partes = ['ALDIPOD', 'CLIENTES']
                ruta_acumulada = ''
                for p in partes:
                    if not p:
                        continue
                    ruta_acumulada = f"{ruta_acumulada}/{p}" if ruta_acumulada else p
                    try:
                        # Intentar navegar
                        ftp.cwd(ruta_acumulada)
                    except:
                        # Si falla, intentar crear
                        try:
                            ftp.mkd(ruta_acumulada)
                            ftp.cwd(ruta_acumulada)
                        except:
                            pass
            
            # Subir al directorio ALDIPOD/CLIENTES
            with open(archivo_local, 'rb') as file:
                ftp.storbinary(f'STOR {nombre_remoto}', file)
            ftp_remote_path = f"ALDIPOD/CLIENTES/{nombre_remoto}"
            print(f"DEBUG FTP: Archivo subido al directorio ALDIPOD/CLIENTES")
        
        else:
            # Si NO es POD, subir al directorio de configuración (para incidencias y MEDIDAS)
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
            
            # Subir al destino principal
            with open(archivo_local, 'rb') as file:
                ftp.storbinary(f'STOR {nombre_remoto}', file)
            ftp_remote_path = f"{destino_principal}/{nombre_remoto}" if destino_principal else nombre_remoto
        
        # Cerrar conexión FTP principal
        ftp.quit()
        
        # Copia local con nombre único (FTP de Nereid mantiene el nombre original)
        nombre_local_unico = añadir_sufijo_aleatorio(nombre_remoto)
        ruta_local_relativa = None
        ok_local, ruta_local_relativa, local_err = guardar_copia_local_backup(
            archivo_local=archivo_local,
            nombre_remoto=nombre_local_unico,
            tipo_documento=tipo_documento
        )
        if ok_local:
            backup_local_ok = True
            print(f"DEBUG BACKUP LOCAL: Copia guardada como {ruta_local_relativa} (FTP: {nombre_remoto})")
        else:
            print(f"WARNING: Error al guardar copia local en VPS: {local_err}")
            nombre_local_unico = nombre_remoto

        # Construir enlace final según dónde esté disponible realmente el archivo.
        if backup_local_ok and ruta_local_relativa:
            enlace_imagen = f"local://{ruta_local_relativa}"
        else:
            enlace_imagen = f"ftp://{config.get('host', 'localhost')}/{ftp_remote_path or nombre_remoto}"

        return True, f"Archivo {nombre_remoto} subido correctamente", enlace_imagen, nombre_local_unico
        
    except ftplib.all_errors as e:
        return False, f"Error FTP: {str(e)}", None, None
    except Exception as e:
        return False, f"Error: {str(e)}", None, None

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
    
    # Todos los clientes usan solo el código de barras sin timestamp (extensión por defecto .jpg)
    return f"{nombre_limpio}.jpg"

def generar_nombre_pdf(codigo_barras: str) -> str:
    """Genera un nombre de archivo PDF a partir del código de barras."""
    caracteres_invalidos = '<>:"/\\|?*'
    nombre_limpio = codigo_barras.strip()
    for char in caracteres_invalidos:
        nombre_limpio = nombre_limpio.replace(char, '_')
    return f"{nombre_limpio}.pdf"


def añadir_sufijo_aleatorio(nombre_archivo: str, digitos: int = 6) -> str:
    """Añade dígitos aleatorios antes de la extensión para evitar sobrescrituras locales."""
    base, ext = os.path.splitext(nombre_archivo)
    sufijo = ''.join(random.choices(string.digits, k=digitos))
    return f"{base}_{sufijo}{ext}"

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

def crear_pdf_temporal(imagenes_base64: List[str], nombre_pdf: str, medidas_por_foto=None, tipo_documento='INCIDENCIA') -> Tuple[bool, str, str]:
    """
    Crea un PDF temporal a partir de una lista de imágenes en base64.
    Cada imagen ocupa la mitad superior de una página A4, centrada, manteniendo proporción.
    Si es tipo 'alb_clientes', la imagen ocupa toda la página A4.
    Si se proporcionan medidas por foto, se añaden debajo de cada imagen correspondiente.
    Devuelve (success, ruta_pdf, error_message)
    """
    print(f"DEBUG: crear_pdf_temporal llamado con medidas_por_foto: {medidas_por_foto}")
    try:
        import base64
        import fitz  # PyMuPDF
        # Directorio temporal
        directorio_temp = 'static/temp_scanner'
        if not os.path.exists(directorio_temp):
            os.makedirs(directorio_temp)

        ruta_pdf = os.path.join(directorio_temp, nombre_pdf)

        # Tamaño A4 en puntos (1pt = 1/72in)
        try:
            a4_rect = fitz.paper_rect("a4")  # disponible en PyMuPDF
            a4_width, a4_height = a4_rect.width, a4_rect.height
        except Exception:
            a4_width, a4_height = 595.2756, 841.8898  # fallback
        
        # Determinar área de imagen según el tipo
        if tipo_documento == 'alb_clientes':
            # Para alb_clientes, usar toda la página
            target_area = fitz.Rect(0, 0, a4_width, a4_height)
        elif tipo_documento == 'POD':
            # Para POD, área fija 21 x 11 cm en la parte superior (ancho completo A4, alto 11cm)
            # A4 de ancho equivale a 21cm; 11cm en puntos:
            alto_11cm_pt = (11 / 2.54) * 72  # 11 cm -> pulgadas -> puntos
            target_area = fitz.Rect(0, 0, a4_width, alto_11cm_pt)
        else:
            # Para otros tipos, usar solo mitad superior
            target_area = fitz.Rect(0, 0, a4_width, a4_height / 2)

        # Crear documento PDF
        pdf_doc = fitz.open()
        for idx, img_b64 in enumerate(imagenes_base64):
            try:
                if 'base64,' in img_b64:
                    img_b64 = img_b64.split('base64,')[1]
                img_bytes = base64.b64decode(img_b64)

                # Crear página A4
                page = pdf_doc.new_page(width=a4_width, height=a4_height)

                # Insertar imagen ajustando a la mitad superior manteniendo aspecto y centrada
                # Primero, obtener dimensiones naturales de la imagen
                # Detectar tipo de imagen por cabecera
                filetype = "jpeg"
                if img_bytes.startswith(b"\x89PNG"):
                    filetype = "png"
                elif img_bytes[6:10] == b"JFIF" or img_bytes.startswith(b"\xff\xd8\xff"):
                    filetype = "jpeg"
                # Abrir imagen para obtener dimensiones
                img_doc = fitz.open(stream=img_bytes, filetype=filetype)
                img_rect = img_doc[0].rect
                img_w, img_h = img_rect.width, img_rect.height
                img_doc.close()

                # Calcular escala para encajar en el área definida manteniendo proporción
                max_w, max_h = target_area.width, target_area.height
                scale = min(max_w / img_w, max_h / img_h)
                draw_w = img_w * scale
                draw_h = img_h * scale
                # Centrar horizontalmente y alinear arriba (y=0) dentro del área
                x0 = (a4_width - draw_w) / 2
                y0 = 0
                target_rect = fitz.Rect(x0, y0, x0 + draw_w, y0 + draw_h)

                # Insertar la imagen desde los bytes
                page.insert_image(target_rect, stream=img_bytes)
                
                # Si hay medidas para esta foto específica, añadirlas debajo de la imagen
                print(f"DEBUG: idx={idx}, tipo={type(idx)}")
                print(f"DEBUG: medidas_por_foto={medidas_por_foto}, tipo={type(medidas_por_foto)}")
                if medidas_por_foto:
                    print(f"DEBUG: len(medidas_por_foto)={len(medidas_por_foto)}")
                    if idx < len(medidas_por_foto):
                        print(f"DEBUG: medidas_por_foto[{idx}]={medidas_por_foto[idx]}")
                
                # Verificación más robusta
                medidas_para_esta_foto = None
                if medidas_por_foto:
                    try:
                        # Convertir idx a entero si es necesario
                        idx_int = int(idx)
                        if idx_int < len(medidas_por_foto) and medidas_por_foto[idx_int] is not None:
                            medidas_para_esta_foto = medidas_por_foto[idx_int]
                            print(f"DEBUG: Medidas encontradas para foto {idx_int + 1}: {medidas_para_esta_foto}")
                    except (ValueError, TypeError, IndexError) as e:
                        print(f"DEBUG: Error accediendo a medidas para foto {idx}: {e}")
                
                if medidas_para_esta_foto:
                    medidas = medidas_para_esta_foto
                    print(f"DEBUG: Añadiendo medidas para foto {idx + 1}: {medidas}")
                    
                    # Formatear texto según el tipo de medidas
                    if medidas.get('alto') == '0' or medidas.get('alto') == 0:
                        # Para POD (solo ancho y largo)
                        medidas_texto = f"Medidas: {medidas['ancho']}cm x {medidas['largo']}cm"
                    else:
                        # Para MEDIDAS (ancho, largo y alto)
                        medidas_texto = f"Medidas: {medidas['ancho']}cm x {medidas['largo']}cm x {medidas['alto']}cm"
                    
                    print(f"DEBUG: Texto de medidas: {medidas_texto}")
                    
                    # Insertar texto con medidas usando método más robusto
                    try:
                        # Calcular posición central horizontal manualmente
                        texto_y = target_rect.y1 + 30  # Más espacio debajo de la imagen
                        
                        # Calcular ancho aproximado del texto para centrarlo
                        texto_ancho_aprox = len(medidas_texto) * 7  # Aproximación
                        texto_x = (a4_width - texto_ancho_aprox) / 2
                        
                        # Asegurar que no se salga de los límites
                        texto_x = max(50, min(texto_x, a4_width - 50))
                        
                        page.insert_text(
                            (texto_x, texto_y),
                            medidas_texto,
                            fontsize=14,
                            color=(0, 0, 0)  # Negro
                        )
                        print(f"DEBUG: Texto insertado con insert_text en posición ({texto_x}, {texto_y})")
                        print(f"DEBUG: Texto: '{medidas_texto}', Ancho aprox: {texto_ancho_aprox}")
                    except Exception as e_texto:
                        print(f"DEBUG: Error con insert_text: {e_texto}")
                        # Fallback con insert_textbox
                        try:
                            texto_rect = fitz.Rect(0, target_rect.y1 + 20, a4_width, target_rect.y1 + 50)
                            page.insert_textbox(
                                texto_rect,
                                medidas_texto,
                                fontsize=12,
                                color=(0, 0, 0),
                                align=fitz.TEXT_ALIGN_CENTER
                            )
                            print(f"DEBUG: Texto insertado con insert_textbox como fallback")
                        except Exception as e_fallback:
                            print(f"DEBUG: Error con fallback: {e_fallback}")
                else:
                    print(f"DEBUG: No hay medidas para la foto {idx + 1}")
            except Exception as e_item:
                # Continuar con el resto aunque una imagen falle
                print(f"WARNING: Error insertando imagen en PDF: {e_item}")
                continue

        pdf_doc.save(ruta_pdf)
        pdf_doc.close()
        return True, ruta_pdf, ''
    except Exception as e:
        return False, '', str(e)

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

def registrar_incidencia(usuario, cliente_id, referencia, nombre_archivo, tipo_documento="INCIDENCIA", medidas=None, observaciones=None, enlace_imagen=None):
    """
    Registra una incidencia en la base de datos
    
    Args:
        usuario: nombre del usuario que sube la imagen
        cliente_id: identificador del cliente (1-8)
        referencia: código de barras escaneado
        nombre_archivo: nombre del archivo subido
        tipo_documento: tipo de documento (INCIDENCIA o MEDIDAS)
        medidas: medidas para el documento (puede ser un diccionario simple o array de medidas por foto)
        observaciones: texto de observaciones opcional
    
    Returns:
        tuple: (success: bool, message: str, incidencia_id: int or None)
    """
    print(f"DEBUG: registrar_incidencia llamado con medidas: {medidas}")
    print(f"DEBUG: tipo de medidas: {type(medidas)}")
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
    
    # Mapeo de usuarios a ubicaciones
    usuarios_merida = ['jmurillo', 'rocio', 'rep', 'oficina', 'almacen', 'fbonilla', 'jmgarcia']
    usuarios_navalmoral = ['repnav', 'yramos']
    
    # Determinar ubicación basada en el usuario
    if usuario in usuarios_navalmoral:
        ubicacion = 'Navalmoral'
    elif usuario in usuarios_merida:
        ubicacion = 'Mérida'
    else:
        ubicacion = 'Mérida'  # Por defecto
    
    print(f"DEBUG: Usuario: {usuario}, Ubicación asignada: {ubicacion}")
    
    nombre_cliente = clientes_map.get(cliente_id, f'Cliente {cliente_id}')
    
    # Si no viene enlace explícito, guardar por defecto en copia local del VPS.
    if not enlace_imagen:
        fecha_hoy = datetime.now().strftime('%Y/%m/%d')
        if tipo_documento == 'POD':
            enlace_imagen = f"local://POD/{fecha_hoy}/{nombre_archivo}"
        elif tipo_documento == 'alb_clientes':
            enlace_imagen = f"local://CLIENTES/{fecha_hoy}/{nombre_archivo}"
        else:
            enlace_imagen = f"local://{fecha_hoy}/{nombre_archivo}"
    
    # NOTA: Las medidas NO deben modificar el nombre del archivo en el enlace
    # El archivo físico se guarda con su nombre original basado en la referencia
    
    try:
        # Obtener fecha/hora actual en zona horaria de España (Europe/Madrid)
        # Esto maneja automáticamente el horario de verano (CEST/CET)
        if ZONEINFO_AVAILABLE:
            # Python 3.9+ con zoneinfo
            tz_madrid = ZoneInfo("Europe/Madrid")
            fecha_actual = datetime.now(tz_madrid)
        elif PYTZ_AVAILABLE:
            # Python con pytz instalado
            tz_madrid = pytz.timezone("Europe/Madrid")
            fecha_actual = datetime.now(tz_madrid)
        else:
            # Fallback: usar fecha local del servidor
            # Asumimos que el servidor está en zona horaria de España
            fecha_actual = datetime.now()
        
        # Normalizar observaciones: None, string vacío, o 'None' -> None
        if observaciones is None:
            obs_final = None
        elif isinstance(observaciones, str):
            obs_clean = observaciones.strip()
            # Si es string vacío o la palabra 'None', convertir a None
            if not obs_clean or obs_clean.lower() == 'none':
                obs_final = None
            else:
                obs_final = obs_clean
        else:
            obs_final = None
        
        print(f"DEBUG: Guardando observaciones en BD: {repr(obs_final)} (tipo: {type(obs_final)})")
        
        incidencia = IncidenciaAldipod(
            fecha=fecha_actual,
            usuario=usuario,
            cliente=nombre_cliente,
            referencia=referencia,
            enlace_imagen=enlace_imagen,
            tipo_documento=tipo_documento,
            ubicacion=ubicacion,
            observaciones=obs_final
        )
        db.session.add(incidencia)
        # Flush para asegurar que se asigne el ID antes del commit
        db.session.flush()
        
        # Verificar que se asignó el ID antes del commit
        incidencia_id = incidencia.id
        if incidencia_id is None:
            print(f"ERROR: Incidencia no obtuvo ID después de flush")
            db.session.rollback()
            return False, "Error: No se pudo asignar ID a la incidencia", None
        
        # Commit explícito
        db.session.commit()
        
        # Verificar nuevamente después del commit
        if incidencia_id is None:
            print(f"ERROR: Incidencia perdió ID después del commit")
            return False, "Error: ID perdido después del commit", None
        
        print(f"DEBUG: Incidencia registrada exitosamente - ID: {incidencia_id}, fecha: {fecha_actual}")
        return True, f"Incidencia registrada correctamente (ID: {incidencia_id})", incidencia_id
        
    except Exception as e:
        error_msg = f"Error al registrar incidencia: {str(e)}"
        print(f"ERROR: {error_msg}")
        import traceback
        print(f"ERROR traceback: {traceback.format_exc()}")
        db.session.rollback()
        return False, error_msg, None

