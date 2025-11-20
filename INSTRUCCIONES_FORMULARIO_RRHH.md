# Instrucciones para Configurar el Formulario RRHH en Web Externa

## 📋 Resumen

Este documento explica cómo configurar un formulario en tu web externa para que envíe los datos al sistema de RRHH de Alditraex.

## 🔗 Endpoint del API

**URL:** `https://tu-dominio.com/api/rrhh/formulario`  
**Método:** `POST`  
**Content-Type:** `multipart/form-data`

> ⚠️ **Nota:** Reemplaza `tu-dominio.com` con la URL real de tu servidor donde está corriendo la aplicación Flask.

## 📝 Campos Requeridos

El formulario debe enviar los siguientes campos:

| Campo | Nombre en el Form | Tipo | Requerido | Descripción |
|-------|-------------------|------|-----------|-------------|
| Nombre completo | `nombre_completo` | texto | ✅ Sí | Nombre completo del candidato |
| Correo electrónico | `correo_electronico` | email | ✅ Sí | Email de contacto |
| Teléfono | `telefono` | texto | ✅ Sí | Número de teléfono |
| Área de interés | `area_interes` | texto | ✅ Sí | Área de trabajo de interés |
| Breve presentación | `presentacion` | texto | ✅ Sí | Texto de presentación del candidato |
| Currículum (PDF) | `curriculum_pdf` | archivo | ❌ Opcional | Archivo PDF del currículum |

## 💻 Ejemplo de Código HTML/JavaScript

### Opción 1: Formulario HTML con JavaScript (Fetch API)

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Formulario de RRHH</title>
</head>
<body>
    <form id="formulario-rrhh">
        <div>
            <label for="nombre_completo">Nombre completo *</label>
            <input type="text" id="nombre_completo" name="nombre_completo" required>
        </div>
        
        <div>
            <label for="correo_electronico">Correo electrónico *</label>
            <input type="email" id="correo_electronico" name="correo_electronico" required>
        </div>
        
        <div>
            <label for="telefono">Teléfono *</label>
            <input type="text" id="telefono" name="telefono" required>
        </div>
        
        <div>
            <label for="area_interes">Área de interés *</label>
            <select id="area_interes" name="area_interes" required>
                <option value="">Seleccione un área</option>
                <option value="Gestión de tráfico">Gestión de tráfico</option>
                <option value="Logística">Logística</option>
                <option value="Administración">Administración</option>
                <option value="Otros">Otros</option>
            </select>
        </div>
        
        <div>
            <label for="presentacion">Breve presentación *</label>
            <textarea id="presentacion" name="presentacion" rows="5" required></textarea>
        </div>
        
        <div>
            <label for="curriculum_pdf">Currículum (PDF)</label>
            <input type="file" id="curriculum_pdf" name="curriculum_pdf" accept=".pdf">
        </div>
        
        <button type="submit">Enviar Formulario</button>
    </form>
    
    <div id="mensaje"></div>

    <script>
        document.getElementById('formulario-rrhh').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const mensajeDiv = document.getElementById('mensaje');
            
            // Mostrar mensaje de carga
            mensajeDiv.innerHTML = '<p>Enviando formulario...</p>';
            mensajeDiv.style.color = 'blue';
            
            try {
                const response = await fetch('https://tu-dominio.com/api/rrhh/formulario', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                if (data.success) {
                    mensajeDiv.innerHTML = '<p style="color: green;">✓ ' + data.message + '</p>';
                    document.getElementById('formulario-rrhh').reset();
                } else {
                    mensajeDiv.innerHTML = '<p style="color: red;">✗ ' + data.message + '</p>';
                }
            } catch (error) {
                mensajeDiv.innerHTML = '<p style="color: red;">✗ Error al enviar el formulario: ' + error.message + '</p>';
            }
        });
    </script>
</body>
</html>
```

### Opción 2: Formulario HTML tradicional (sin JavaScript)

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Formulario de RRHH</title>
</head>
<body>
    <form action="https://tu-dominio.com/api/rrhh/formulario" method="POST" enctype="multipart/form-data">
        <div>
            <label for="nombre_completo">Nombre completo *</label>
            <input type="text" id="nombre_completo" name="nombre_completo" required>
        </div>
        
        <div>
            <label for="correo_electronico">Correo electrónico *</label>
            <input type="email" id="correo_electronico" name="correo_electronico" required>
        </div>
        
        <div>
            <label for="telefono">Teléfono *</label>
            <input type="text" id="telefono" name="telefono" required>
        </div>
        
        <div>
            <label for="area_interes">Área de interés *</label>
            <select id="area_interes" name="area_interes" required>
                <option value="">Seleccione un área</option>
                <option value="Gestión de tráfico">Gestión de tráfico</option>
                <option value="Logística">Logística</option>
                <option value="Administración">Administración</option>
                <option value="Otros">Otros</option>
            </select>
        </div>
        
        <div>
            <label for="presentacion">Breve presentación *</label>
            <textarea id="presentacion" name="presentacion" rows="5" required></textarea>
        </div>
        
        <div>
            <label for="curriculum_pdf">Currículum (PDF)</label>
            <input type="file" id="curriculum_pdf" name="curriculum_pdf" accept=".pdf">
        </div>
        
        <button type="submit">Enviar Formulario</button>
    </form>
</body>
</html>
```

> ⚠️ **Nota:** Con el formulario tradicional, el navegador redirigirá a la respuesta JSON. Es mejor usar la Opción 1 con JavaScript para una mejor experiencia de usuario.

## 🔧 Configuración CORS (si es necesario)

Si tu web externa está en un dominio diferente y encuentras errores de CORS, necesitarás instalar `flask-cors` y configurarlo:

### 1. Instalar flask-cors

```bash
pip install flask-cors
```

### 2. Modificar `rrhh/rrhh_routes.py`

Añade al inicio del archivo:

```python
from flask_cors import CORS, cross_origin
```

Y en la función `register_rrhh_routes`:

```python
def register_rrhh_routes(app):
    """Registra las rutas para el formulario de RRHH."""
    
    # Habilitar CORS para esta ruta específica
    CORS(app, resources={r"/api/rrhh/*": {"origins": "*"}})
    
    @app.route('/api/rrhh/formulario', methods=['POST'])
    @cross_origin()
    def procesar_formulario_rrhh():
        # ... resto del código ...
```

## 📨 Respuestas del API

### Éxito (200 OK)

```json
{
    "success": true,
    "message": "Formulario recibido y correo enviado correctamente."
}
```

### Error - Datos incompletos (400 Bad Request)

```json
{
    "success": false,
    "message": "Datos del formulario incompletos: Faltan campos obligatorios en el formulario: Nombre completo"
}
```

### Error - Archivo no válido (400 Bad Request)

```json
{
    "success": false,
    "message": "El archivo del currículum debe ser un PDF (.pdf)"
}
```

### Error - Servidor (500 Internal Server Error)

```json
{
    "success": false,
    "message": "Error al procesar el formulario: [descripción del error]"
}
```

## ✅ Validaciones

El sistema valida automáticamente:

- ✅ Todos los campos requeridos están presentes
- ✅ El archivo PDF (si se envía) tiene extensión `.pdf`
- ✅ La configuración SMTP está correcta
- ✅ El correo se puede enviar correctamente

## 🔍 Pruebas

Para probar el endpoint, puedes usar `curl`:

```bash
curl -X POST https://tu-dominio.com/api/rrhh/formulario \
  -F "nombre_completo=Juan Pérez" \
  -F "correo_electronico=juan@ejemplo.com" \
  -F "telefono=654654654" \
  -F "area_interes=Gestión de tráfico" \
  -F "presentacion=Esta es una prueba" \
  -F "curriculum_pdf=@/ruta/al/archivo.pdf"
```

## 📧 Destinatario del Correo

Los correos se envían automáticamente a: **jmurillo@alditraex.es**  
Desde: **rrhh@alditraex.es**

## 🆘 Solución de Problemas

### Error: "CORS policy: No 'Access-Control-Allow-Origin' header"
- **Solución:** Instala y configura `flask-cors` como se explica arriba.

### Error: "Método no permitido"
- **Solución:** Asegúrate de usar `POST` y no `GET`.

### Error: "Datos del formulario incompletos"
- **Solución:** Verifica que todos los campos requeridos estén presentes y tengan valores.

### Error: "El archivo del currículum debe ser un PDF"
- **Solución:** Solo se aceptan archivos con extensión `.pdf`.

## 📞 Soporte

Si tienes problemas, verifica:
1. Que la URL del endpoint sea correcta
2. Que el servidor Flask esté corriendo
3. Que la configuración SMTP esté correcta en `rrhh_mailer.py`
4. Los logs del servidor para ver errores detallados

