# 🏢 Clientes y Logos - Scanner FTP

## 📋 Distribución de Clientes

Los 8 contenedores del scanner están ahora personalizados con los logos de cada cliente:

### Contenedor 1: XPO Logistics
- **Logo**: `static/scanner/logoxpologistics.jpg`
- **ID Cliente**: 1
- **Carpeta FTP**: `cliente_1/`

### Contenedor 2: Surpaq
- **Logo**: `static/scanner/logosurpaq.jpg`
- **ID Cliente**: 2
- **Carpeta FTP**: `cliente_2/`

### Contenedor 3: TSB
- **Logo**: `static/scanner/tsb.jpg`
- **ID Cliente**: 3
- **Carpeta FTP**: `cliente_3/`

### Contenedor 4: Alditraex
- **Logo**: `static/scanner/alditraex.png`
- **ID Cliente**: 4
- **Carpeta FTP**: `cliente_4/`

### Contenedor 5: NTL
- **Logo**: `static/scanner/ntl.jpg`
- **ID Cliente**: 5
- **Carpeta FTP**: `cliente_5/`

### Contenedor 6: Simões
- **Logo**: `static/scanner/simoes.jpg`
- **ID Cliente**: 6
- **Carpeta FTP**: `cliente_6/`

### Contenedor 7: Esser
- **Logo**: `static/scanner/esser.webp`
- **ID Cliente**: 7
- **Carpeta FTP**: `cliente_7/`

### Contenedor 8: BD Trans
- **Logo**: `static/scanner/bdtrans.png`
- **ID Cliente**: 8
- **Carpeta FTP**: `cliente_8/`

---

## 🎨 Características de Diseño

### Logos
- **Tamaño máximo**: 120px ancho × 80px alto
- **Formato**: Ajustado automáticamente manteniendo proporciones
- **Estilo**: Bordes redondeados (8px)
- **Posición**: Centrado en la parte superior de cada tarjeta

### Tarjetas de Cliente
- **Diseño**: Flexbox vertical centrado
- **Efecto hover**: Elevación con sombra
- **Colores**: Fondo blanco, texto principal en morado (#667eea)
- **Espaciado**: Grid responsive con gap de 20px

### Responsive
- **Desktop**: 4 columnas (en pantallas grandes)
- **Tablet**: 2-3 columnas (ajuste automático)
- **Móvil**: 1-2 columnas (según ancho)

---

## 📁 Estructura de Archivos FTP

Cuando se sube una imagen, se organiza de la siguiente forma:

```
servidor_ftp/
├── cliente_1/  (XPO Logistics)
│   ├── CODIGO123_20251009_120530.jpg
│   └── CODIGO456_20251009_121045.jpg
├── cliente_2/  (Surpaq)
│   └── CODIGO789_20251009_122000.jpg
├── cliente_3/  (TSB)
│   └── CODIGO321_20251009_123000.jpg
├── cliente_4/  (Alditraex)
│   └── CODIGO654_20251009_124000.jpg
├── cliente_5/  (NTL)
│   └── CODIGO987_20251009_125000.jpg
├── cliente_6/  (Simões)
│   └── CODIGO147_20251009_130000.jpg
├── cliente_7/  (Esser)
│   └── CODIGO258_20251009_131000.jpg
└── cliente_8/
    └── CODIGO369_20251009_132000.jpg
```

---

## 🔄 Cómo Añadir o Cambiar un Logo

### Para añadir un nuevo logo al Cliente 8:

1. **Coloca el archivo** en: `static/scanner/`
   - Ejemplo: `static/scanner/nuevo_cliente.jpg`

2. **Edita** `templates/scanner_clientes.html`:
   ```html
   <div class="cliente-card" onclick="abrirScanner(8)">
       <img src="{{ url_for('static', filename='scanner/nuevo_cliente.jpg') }}" 
            alt="Nuevo Cliente" class="cliente-logo">
       <h2>Nuevo Cliente</h2>
       <p>Click para escanear</p>
   </div>
   ```

3. **Actualiza el JavaScript** (mapeo de nombres):
   ```javascript
   const nombresClientes = {
       // ... otros clientes
       8: 'Nuevo Cliente'
   };
   ```

### Para cambiar un logo existente:

1. **Reemplaza el archivo** en `static/scanner/`
2. **Reinicia el servidor** (si está en modo producción)
3. **Limpia la caché** del navegador si es necesario

---

## 🎯 Formatos de Logo Recomendados

### Formatos Soportados
- ✅ **JPG/JPEG** - Recomendado para fotos
- ✅ **PNG** - Recomendado para logos con transparencia
- ✅ **WEBP** - Formato moderno, buena compresión
- ⚠️ **GIF** - Funciona pero no recomendado
- ❌ **SVG** - No recomendado (usar PNG en su lugar)

### Dimensiones Recomendadas
- **Ancho**: 240px - 480px
- **Alto**: 160px - 320px
- **Ratio**: 3:2 o 16:9 (horizontal)
- **Peso**: Menos de 100KB para carga rápida

### Consejos de Calidad
- Usa fondo transparente (PNG) si es posible
- Optimiza las imágenes antes de subirlas
- Mantén buena resolución (72-150 DPI)
- Usa nombres descriptivos: `nombrecliente.jpg`

---

## 🔧 Personalización Avanzada

### Cambiar el Cliente en el Modal

El nombre que aparece en el modal se controla desde JavaScript:

```javascript
const nombresClientes = {
    1: 'XPO Logistics',
    2: 'Surpaq',
    // ... personaliza aquí
};
```

### Configuración FTP por Cliente

Para configurar diferentes servidores FTP por cliente, modifica:
`scanner_ftp/funciones_scanner.py`

Ejemplo:
```python
def obtener_config_ftp_cliente(cliente_id):
    configs = {
        1: {'host': 'ftp1.ejemplo.com', ...},
        2: {'host': 'ftp2.ejemplo.com', ...},
    }
    return configs.get(cliente_id, config_default)
```

---

## 📝 Notas

- Los logos se cargan dinámicamente desde Flask usando `url_for()`
- El sistema es escalable: añade más clientes modificando el HTML
- Cada cliente tiene su propia carpeta en el FTP para organización
- Los nombres de clientes se mantienen en el código para fácil mantenimiento

---

## ✅ Estado Actual

- ✅ 8 clientes con logos personalizados
- ✅ Sistema de organización FTP implementado
- ✅ Diseño responsive y moderno
- ✅ Identificación visual clara por cliente

---

**Última actualización**: Octubre 2025

