# ⌨️ Nueva Funcionalidad: Entrada Manual de Códigos

## ✅ Cambios Implementados

Se ha añadido la opción de **introducir códigos de barras manualmente** con el teclado como alternativa al escaneo con cámara.

## 🎯 Características

### 1. **Dos Modos de Entrada**

#### Modo Automático (Cámara)
- Escaneo automático con la cámara del dispositivo
- Detección automática de códigos de barras
- Ideal para uso con móviles

#### Modo Manual (Teclado) ⭐ NUEVO
- Introducción manual del código con teclado
- Compatible con lectores de códigos de barras USB
- Alternativa cuando la cámara no está disponible o no funciona
- Presionar **Enter** para confirmar rápidamente

### 2. **Flujo de Usuario Mejorado**

```
┌─────────────────────────────────┐
│  Seleccionar Cliente (1-8)      │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│  Se abre la cámara automática   │
│  [⌨️ Introducir Manualmente]    │ ◄── NUEVO BOTÓN
│  [Cancelar]                      │
└────────────┬────────────────────┘
             │
     ┌───────┴────────┐
     │                │
     ▼                ▼
┌─────────┐    ┌──────────────┐
│ Cámara  │    │ Input Manual │ ◄── NUEVO
│ Escanea │    │ Escribe código│
└────┬────┘    └──────┬───────┘
     │                │
     └───────┬────────┘
             ▼
   ┌─────────────────────┐
   │ Confirmar Código    │
   │ [✓ Correcto]        │
   │ [✗ Reintentar]      │
   └─────────┬───────────┘
             │
             ▼
   ┌─────────────────────┐
   │  Tomar Foto         │
   │  Enviar a FTP       │
   └─────────────────────┘
```

### 3. **Casos de Uso**

✅ **Cuando usar entrada manual:**
- La cámara no funciona o no está disponible
- Problemas de permisos de cámara
- Códigos difíciles de escanear (dañados, pequeños, reflectantes)
- Uso de lectores de códigos de barras USB/Bluetooth
- Entornos con poca luz
- Preferencia del usuario

✅ **Cuando usar escaneo automático:**
- Dispositivo móvil con buena cámara
- Códigos de barras en buen estado
- Buena iluminación
- Mayor rapidez (no requiere escribir)

## 🎨 Interfaz de Usuario

### Botón "⌨️ Introducir Manualmente"
- Aparece junto con la vista de la cámara
- Color distintivo (azul primario)
- Icono de teclado para fácil identificación

### Pantalla de Entrada Manual
- Campo de texto grande y claro
- Placeholder: "Escribe el código aquí..."
- Autofocus automático
- Detección de tecla **Enter** para confirmar rápidamente
- Botones:
  - ✓ **Confirmar Código** (verde)
  - 📷 **Volver a Escanear** (gris)
  - **Cancelar** (gris)

## 🔄 Transiciones

- Cambio suave entre modo cámara y modo manual
- El escáner de cámara se detiene al cambiar a manual
- Limpieza automática del campo al cerrar o cancelar
- Validación: el código no puede estar vacío

## 💡 Ventajas

1. **Mayor Flexibilidad**: Funciona incluso sin cámara
2. **Compatibilidad**: Soporta lectores USB/Bluetooth
3. **Accesibilidad**: Algunos usuarios prefieren escribir
4. **Respaldo**: Si el escaneo falla, siempre hay alternativa
5. **Dispositivos sin Cámara**: PCs de escritorio, tablets antiguas

## 🧪 Probar la Funcionalidad

1. Accede a: `http://192.168.1.7:5000/scanner_clientes`
2. Selecciona un cliente
3. Haz clic en **"⌨️ Introducir Manualmente"**
4. Escribe un código (ej: "TEST123")
5. Presiona **Enter** o clic en **"✓ Confirmar Código"**
6. Continúa con el flujo normal (tomar foto y enviar)

## 📝 Notas Técnicas

- El campo acepta cualquier texto (alfanumérico)
- Validación mínima: no vacío, mínimo 3 caracteres (del backend)
- El código se trata igual que uno escaneado
- Los caracteres especiales se limpian automáticamente al guardar
- El timestamp se añade para evitar duplicados

## 🔐 Seguridad

- Validación en cliente y servidor
- Limpieza de caracteres no permitidos en nombres de archivo
- Mismo nivel de validación que códigos escaneados

## 🚀 Mejoras Futuras Posibles

- [ ] Añadir validación de formato (EAN-13, UPC, etc.)
- [ ] Historial de códigos recientes
- [ ] Sugerencias automáticas
- [ ] Escaneo mediante foto (además de video)
- [ ] Soporte para QR codes

═══════════════════════════════════════════════════════════

✅ **La funcionalidad está lista para usar.**
✅ **Compatible con todos los navegadores.**
✅ **No requiere permisos de cámara para modo manual.**

