# Módulo Scanner FTP

Este módulo permite escanear códigos de barras y subir imágenes a un servidor FTP.

## Características

- **8 Contenedores de Cliente**: Cada uno representa un cliente diferente y permite configuraciones separadas en el futuro
- **Escaneo de Códigos de Barras**: Utiliza la cámara del dispositivo para leer códigos de barras automáticamente
- **Captura de Fotos**: Después de escanear el código, permite tomar una foto del producto
- **Subida a FTP**: Las imágenes se suben automáticamente al servidor FTP con el nombre del código de barras escaneado
- **Organización por Cliente**: Las imágenes se organizan en carpetas según el cliente (cliente_1, cliente_2, etc.)

## Flujo de Trabajo

1. El usuario hace clic en uno de los 8 contenedores de cliente
2. Se abre la cámara en modo escáner de códigos de barras
   - **Opción A**: Escanear automáticamente con la cámara
   - **Opción B**: Hacer clic en "⌨️ Introducir Manualmente" para escribir el código con el teclado
3. Al detectar o introducir un código, se muestra para confirmación
4. Una vez confirmado, se abre la cámara para tomar una foto
5. Se muestra la foto para confirmación
6. Al confirmar, la imagen se sube al FTP con el nombre del código de barras + timestamp

## Archivos

- `scanner_ftp.py`: Rutas Flask principales
- `funciones_scanner.py`: Funciones auxiliares para FTP, validación y procesamiento de imágenes
- `templates/scanner_clientes.html`: Interfaz de usuario con los 8 contenedores

## Configuración FTP

La configuración del servidor FTP debe estar en `static/ftp_config.json` con el siguiente formato:

```json
{
    "host": "tu-servidor-ftp.com",
    "port": 21,
    "user": "usuario",
    "password": "contraseña",
    "directory": "/ruta/destino"
}
```

## Tecnologías Utilizadas

- **ZXing**: Librería JavaScript para escaneo de códigos de barras
- **MediaDevices API**: Para acceso a la cámara del dispositivo
- **ftplib**: Librería Python para conexión FTP
- **Flask**: Framework web

## Requisitos

- Navegador con soporte para `getUserMedia` (Chrome, Firefox, Safari moderno)
- Permisos de cámara habilitados
- Servidor FTP configurado y accesible
- Conexión HTTPS recomendada para acceso a la cámara en producción

## Uso

1. Accede a la ruta `/scanner_clientes` después de iniciar sesión
2. Selecciona uno de los 8 clientes
3. Permite el acceso a la cámara cuando se solicite
4. Sigue las instrucciones en pantalla para escanear y fotografiar

## Limpieza Automática

El sistema limpia automáticamente los archivos temporales que tienen más de 1 hora de antigüedad para evitar el uso excesivo de espacio en disco.

## Personalización Futura

Cada uno de los 8 contenedores puede ser personalizado independientemente para:
- Diferentes configuraciones FTP
- Diferentes validaciones de códigos de barras
- Diferentes formatos de nombre de archivo
- Metadatos adicionales por cliente

