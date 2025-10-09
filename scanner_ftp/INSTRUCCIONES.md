# Instrucciones de Uso - Scanner FTP

## Acceso al Sistema

1. Inicia sesión en la aplicación con tu usuario y contraseña
2. Desde el menú principal, accede a `/scanner_clientes` o agrega un enlace en el menú de navegación

## Proceso Paso a Paso

### Paso 1: Seleccionar Cliente
- La pantalla muestra 8 contenedores, uno para cada cliente
- Haz clic en el contenedor del cliente con el que vas a trabajar
- Se abrirá el modal del escáner

### Paso 2: Escanear o Introducir Código de Barras

Tienes **dos opciones** para ingresar el código:

#### Opción A: Escaneo Automático (con cámara)
- Se activará automáticamente la cámara del dispositivo
- Apunta la cámara hacia el código de barras
- La aplicación detectará y leerá el código automáticamente
- Una vez detectado, se mostrará en pantalla para confirmación

#### Opción B: Introducción Manual (con teclado)
- Haz clic en **"⌨️ Introducir Manualmente"**
- Escribe el código de barras con el teclado
- Puedes usar un lector de códigos de barras USB que actúa como teclado
- Presiona **Enter** o haz clic en **"✓ Confirmar Código"**
- También puedes volver a la opción de escaneo con **"📷 Volver a Escanear"**

**Opciones de Confirmación:**
- ✓ **Código Correcto**: Continúa al siguiente paso
- ✗ **Reintentar**: Vuelve a escanear o introducir el código de barras

### Paso 3: Tomar Fotografía
- Una vez confirmado el código, se abrirá nuevamente la cámara
- Apunta la cámara hacia el objeto que deseas fotografiar
- Haz clic en **📷 Capturar Foto**
- Se mostrará una vista previa de la foto tomada

**Opciones:**
- ✓ **Enviar a FTP**: Sube la imagen al servidor
- ✗ **Repetir Foto**: Toma otra fotografía

### Paso 4: Confirmación de Envío
- La aplicación subirá la imagen al servidor FTP
- La imagen se guardará con el nombre del código de barras escaneado
- Se mostrará un mensaje de éxito o error
- Haz clic en **✓ Finalizar** para cerrar el proceso

## Organización de Archivos

Las imágenes se guardan en el servidor FTP con la siguiente estructura:

```
/directorio_ftp/
  ├── cliente_1/
  │   ├── CODIGO123_20251009_120530.jpg
  │   └── CODIGO456_20251009_120645.jpg
  ├── cliente_2/
  │   └── CODIGO789_20251009_121000.jpg
  ...
```

## Nombre de Archivos

Formato: `CODIGO_BARRAS_AAAAMMDD_HHMMSS.jpg`

Ejemplo: `ABC123456_20251009_143025.jpg`
- **ABC123456**: Código de barras escaneado
- **20251009**: Fecha (9 de octubre de 2025)
- **143025**: Hora (14:30:25)

## Permisos Necesarios

### En el Navegador:
- **Cámara**: Requerido para escanear códigos y tomar fotos
- **HTTPS**: Recomendado para producción (algunos navegadores solo permiten acceso a la cámara en sitios seguros)

### Navegadores Compatibles:
- ✓ Google Chrome (recomendado)
- ✓ Firefox
- ✓ Safari (iOS 11+)
- ✓ Microsoft Edge
- ✗ Internet Explorer (no compatible)

## Solución de Problemas

### La cámara no se activa
1. Verifica que el navegador tenga permisos de cámara
2. Asegúrate de estar usando HTTPS (en producción)
3. Cierra otras aplicaciones que puedan estar usando la cámara
4. Recarga la página y vuelve a intentar

### El código de barras no se detecta
1. Asegúrate de que haya buena iluminación
2. Mantén el código de barras estable frente a la cámara
3. Verifica que el código esté completo y legible
4. Prueba acercando o alejando el código

### Error al subir la imagen
1. Verifica la conexión a internet
2. Asegúrate de que el servidor FTP esté accesible
3. Verifica las credenciales del FTP en `static/ftp_config.json`
4. Contacta al administrador del sistema si el problema persiste

### La imagen se sube pero no aparece en el servidor
1. Verifica que el directorio de destino exista en el servidor FTP
2. Comprueba que tengas permisos de escritura en el directorio
3. Revisa los logs del servidor para más información

## Consejos de Uso

### Para mejores resultados al escanear:
- Usa buena iluminación
- Mantén el código de barras plano y sin arrugas
- Evita reflejos en códigos plastificados
- Mantén una distancia de 10-30 cm

### Para mejores fotografías:
- Usa iluminación uniforme
- Asegúrate de que el objeto esté bien enfocado
- Toma la foto desde un ángulo apropiado
- Verifica la vista previa antes de enviar

## Características Adicionales

### Limpieza Automática
El sistema elimina automáticamente archivos temporales mayores a 1 hora para mantener el espacio en disco.

### Validación de Códigos
El sistema valida que los códigos de barras tengan al menos 3 caracteres y no estén vacíos.

### Nombres de Archivo Seguros
Los caracteres especiales en códigos de barras se reemplazan automáticamente por guiones bajos (_) para evitar problemas en el sistema de archivos.

## Contacto y Soporte

Si encuentras problemas o necesitas ayuda adicional, contacta al administrador del sistema.

