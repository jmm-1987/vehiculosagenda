"""
Módulo para generar PDFs de presupuestos
"""
import os
import fitz  # PyMuPDF
from datetime import datetime

# Datos de la empresa
EMPRESA_NOMBRE = "Alditraex, S.L."
EMPRESA_DIRECCION = "Pol. Ind. Prado C/Valladolid parc. R46 A/b, 06800 Mérida - Badajoz"
EMPRESA_CIF = "B06422208"
EMPRESA_CUENTA_BANCARIA = "ES38 0078 0076 4440 0000 3347"

# Política de privacidad (texto completo del PDF)
TEXTO_PRIVACIDAD = """De conformidad con lo establecido en la normativa vigente en Protección de Datos de Carácter Personal, le informamos que los datos de carácter personal que nos proporcione serán incorporados a un fichero titularidad de ALDITRAEX, S.L. con la finalidad de gestionar la relación comercial, contractual y administrativa, así como para remitirle información comercial sobre nuestros productos y servicios. Los datos no serán cedidos a terceros salvo obligación legal. Puede ejercitar sus derechos de acceso, rectificación, supresión, portabilidad, limitación y oposición dirigiéndose a la dirección postal arriba indicada o al correo electrónico jmurillo@alditraex.es. Asimismo, tiene derecho a presentar una reclamación ante la Agencia Española de Protección de Datos (www.aepd.es) si considera que el tratamiento de sus datos personales vulnera la normativa vigente."""

# Observaciones del presupuesto
OBSERVACIONES_PRESUPUESTO = """VALIDEZ DEL PRESUPUESTO: 15 DÍAS DESDE SU COMUNICACIÓN:

MUY IMPORTANTE A TENER EN CUENTA PARA ACEPTACIÓN DE PRESUPUESTO
La mercancía debe estar perfectamente embalada, paletizada para ser transportada en nuestra red.

**Esta mercancía transportada no es cubierta por nuestro seguro. Con lo cual, cualquier avería o daño, pérdida que surja en estas tipologías o similares en caso de aceptación de servicio no serán admitidas sus reclamaciones por parte de Alditraex.

*No entramos en fincas, nuestras entregas y recogidas son puerta a puerta.-

"Si el bulto una vez recibido en nuestro almacén difiriera de las medidas y pesos que nos han dicho ustedes en la petición del servicio, deben saber que primaran las medidas y pesos tomadas en nuestras instalaciones para el precio del servicio a pagar.

En el caso de estar de acuerdo con la cotización ofrecida, rogamos hagan el ingreso por transferencia al mismo a la cuenta nº ES38 0078 0076 4440 0000 3347 (adjunten copia de la misma a este email) para poder poner en marcha el servicio. Quedamos a la espera de sus indicaciones."""


def generar_pdf_presupuesto(presupuesto, cliente, output_path=None):
    """
    Genera un PDF del presupuesto con el formato especificado.
    
    Args:
        presupuesto: Objeto Presupuesto
        cliente: Objeto ClientePresupuesto
        output_path: Ruta donde guardar el PDF. Si es None, retorna los bytes del PDF en memoria
    
    Returns:
        bytes o str: Bytes del PDF si output_path es None, o ruta del archivo si se proporciona output_path
    """
    # Si no se proporciona output_path, generamos en memoria
    generar_en_memoria = output_path is None
    
    # Crear documento PDF A4
    doc = fitz.open()
    page = doc.new_page(width=595.2756, height=841.8898)  # A4 en puntos
    
    # Configuración de fuentes y tamaños
    font_size_title = 16
    font_size_header = 12
    font_size_normal = 10
    font_size_small = 8
    
    # Cargar logo
    logo_path = 'static/logo.png'
    if os.path.exists(logo_path):
        try:
            img_rect = fitz.Rect(50, 30, 200, 80)  # Posición del logo (se mantiene igual)
            page.insert_image(img_rect, filename=logo_path)
        except Exception as e:
            print(f"Error al insertar logo: {e}")
    
    # === INFORMACIÓN DE LA EMPRESA (izquierda) ===
    y_pos = 150 + (12 * 5)  # Bajar 5 líneas más (120 + 60 = 180)
    page.insert_text((50, y_pos), EMPRESA_NOMBRE, fontsize=font_size_header, color=(0, 0, 0))
    y_pos += 15
    page.insert_text((50, y_pos), EMPRESA_DIRECCION, fontsize=font_size_normal, color=(0, 0, 0))
    y_pos += 12
    page.insert_text((50, y_pos), f"CIF/NIF: {EMPRESA_CIF}", fontsize=font_size_normal, color=(0, 0, 0))
    
    # === INFORMACIÓN DEL CLIENTE (derecha) ===
    y_pos_cliente = 120  # Bajar más desde 100 a 120
    page.insert_text((350, y_pos_cliente), "CLIENTE:", fontsize=font_size_normal, color=(0, 0, 0))
    y_pos_cliente += 12
    page.insert_text((350, y_pos_cliente), f"Nombre: {cliente.nombre}", fontsize=font_size_normal, color=(0, 0, 0))
    y_pos_cliente += 12
    page.insert_text((350, y_pos_cliente), f"Dirección: {cliente.direccion}", fontsize=font_size_normal, color=(0, 0, 0))
    y_pos_cliente += 12
    if cliente.poblacion:
        page.insert_text((350, y_pos_cliente), f"Población: {cliente.poblacion}", fontsize=font_size_normal, color=(0, 0, 0))
        y_pos_cliente += 12
    page.insert_text((350, y_pos_cliente), "Provincia:", fontsize=font_size_normal, color=(0, 0, 0))
    y_pos_cliente += 12
    page.insert_text((350, y_pos_cliente), f"CIF/NIF: {cliente.cif}", fontsize=font_size_normal, color=(0, 0, 0))
    
    # === INFORMACIÓN DEL PRESUPUESTO (derecha, debajo del cliente) ===
    y_pos_presupuesto = y_pos_cliente + 20
    fecha_str = presupuesto.fecha_presupuesto.strftime('%d/%m/%Y') if presupuesto.fecha_presupuesto else ""
    page.insert_text((350, y_pos_presupuesto), f"FECHA PRESUPUESTO: {fecha_str}", fontsize=font_size_normal, color=(0, 0, 0))
    y_pos_presupuesto += 12
    page.insert_text((350, y_pos_presupuesto), f"N°: {presupuesto.numero_presupuesto}", fontsize=font_size_normal, color=(0, 0, 0))
    y_pos_presupuesto += 12
    concepto_titulo = presupuesto.concepto[:30] if presupuesto.concepto else "Presupuesto"
    page.insert_text((350, y_pos_presupuesto), f"PRESUPUESTO {concepto_titulo}", fontsize=font_size_normal, color=(0, 0, 0))
    
    # === TABLA DE CONCEPTOS ===
    y_tabla = y_pos_presupuesto + 40
    
    # Encabezados de la tabla
    headers = ["N°", "CONCEPTO", "PRECIO", "% IVA", "IVA", "TOTAL"]
    col_widths = [30, 250, 70, 50, 70, 80]
    x_start = 50
    x_positions = [x_start]
    for i in range(len(col_widths) - 1):
        x_positions.append(x_positions[i] + col_widths[i])
    
    # Dibujar encabezados
    y_header = y_tabla
    for i, header in enumerate(headers):
        page.insert_text((x_positions[i] + 5, y_header), header, fontsize=font_size_small, color=(0, 0, 0))
    
    # Línea debajo de los encabezados
    page.draw_line((x_start, y_header + 5), (x_start + sum(col_widths), y_header + 5), color=(0, 0, 0), width=1)
    
    # Calcular IVA percent
    iva_percent = 0
    if presupuesto.importe and presupuesto.importe > 0:
        iva_percent = (presupuesto.iva / presupuesto.importe) * 100
    
    # Fila de datos
    y_row = y_header + 20
    page.insert_text((x_positions[0] + 5, y_row), "1", fontsize=font_size_normal, color=(0, 0, 0))
    
    # Concepto (puede ser largo, ajustar)
    concepto_texto = presupuesto.concepto if presupuesto.concepto else ""
    # Truncar si es muy largo
    if len(concepto_texto) > 50:
        concepto_texto = concepto_texto[:47] + "..."
    page.insert_text((x_positions[1] + 5, y_row), concepto_texto, fontsize=font_size_normal, color=(0, 0, 0))
    
    # Precio
    precio_str = f"{presupuesto.importe:.2f}"
    page.insert_text((x_positions[2] + 5, y_row), precio_str, fontsize=font_size_normal, color=(0, 0, 0))
    
    # % IVA
    iva_percent_str = f"{iva_percent:.0f}"
    page.insert_text((x_positions[3] + 5, y_row), iva_percent_str, fontsize=font_size_normal, color=(0, 0, 0))
    
    # IVA
    iva_str = f"{presupuesto.iva:.2f}"
    page.insert_text((x_positions[4] + 5, y_row), iva_str, fontsize=font_size_normal, color=(0, 0, 0))
    
    # Total
    total_str = f"{presupuesto.total:.2f}"
    page.insert_text((x_positions[5] + 5, y_row), total_str, fontsize=font_size_normal, color=(0, 0, 0))
    
    # Línea debajo de la fila
    y_row_bottom = y_row + 15
    page.draw_line((x_start, y_row_bottom), (x_start + sum(col_widths), y_row_bottom), color=(0, 0, 0), width=1)
    
    # === OBSERVACIONES ===
    y_obs = y_row_bottom + 30
    page.insert_text((50, y_obs), "OBSERVACIONES:", fontsize=font_size_header, color=(0, 0, 0))
    y_obs += 20
    
    # Insertar observaciones del presupuesto (pueden ser largas, usar texto multilínea)
    def insertar_texto_multilinea(texto, x, y_start, max_chars_per_line, fontsize):
        """Función auxiliar para insertar texto multilínea"""
        words = texto.split(' ')
        current_line = ""
        y_current = y_start
        for word in words:
            test_line = current_line + word + " " if current_line else word + " "
            if len(test_line) > max_chars_per_line and current_line:
                page.insert_text((x, y_current), current_line.strip(), fontsize=fontsize, color=(0, 0, 0))
                y_current += fontsize + 2
                current_line = word + " "
            else:
                current_line = test_line
        if current_line.strip():
            page.insert_text((x, y_current), current_line.strip(), fontsize=fontsize, color=(0, 0, 0))
            y_current += fontsize + 2
        return y_current
    
    obs_lines = OBSERVACIONES_PRESUPUESTO.split('\n')
    for line in obs_lines:
        if line.strip():
            y_obs = insertar_texto_multilinea(line.strip(), 50, y_obs, 90, font_size_small)
            y_obs += 5  # Espacio entre párrafos
    
    # === RESUMEN (cuadro derecho) ===
    y_resumen = y_tabla + 50
    x_resumen = 400
    
    # Caja de resumen
    box_height = 60
    box_width = 150
    box_rect = fitz.Rect(x_resumen, y_resumen, x_resumen + box_width, y_resumen + box_height)
    page.draw_rect(box_rect, color=(0, 0, 0), width=1)
    
    # Texto dentro del resumen
    y_resumen_text = y_resumen + 15
    page.insert_text((x_resumen + 5, y_resumen_text), f"Sujeto a retención: {presupuesto.importe:.2f} €", fontsize=font_size_small, color=(0, 0, 0))
    y_resumen_text += 15
    page.insert_text((x_resumen + 5, y_resumen_text), f"IVA: {presupuesto.iva:.2f} €", fontsize=font_size_small, color=(0, 0, 0))
    y_resumen_text += 15
    page.insert_text((x_resumen + 5, y_resumen_text), f"Total: {presupuesto.total:.2f} €", fontsize=font_size_small, color=(0, 0, 0))
    
    # === POLÍTICA DE PRIVACIDAD (parte inferior) ===
    y_privacidad = 800  # Bajar un poco más para que no se corte
    # Dividir el texto de privacidad en líneas
    privacidad_lines = TEXTO_PRIVACIDAD.split('. ')
    y_priv = y_privacidad
    for line in privacidad_lines[:3]:  # Mostrar primeras líneas principales
        if line.strip():
            if len(line) > 120:
                words = line.split(' ')
                current_line = ""
                for word in words:
                    if len(current_line + word) < 120:
                        current_line += word + " "
                    else:
                        if current_line:
                            page.insert_text((50, y_priv), current_line.strip() + ".", fontsize=7, color=(0, 0, 0))
                            y_priv += 10
                        current_line = word + " "
                if current_line:
                    page.insert_text((50, y_priv), current_line.strip() + ".", fontsize=7, color=(0, 0, 0))
                    y_priv += 10
            else:
                page.insert_text((50, y_priv), line.strip() + ".", fontsize=7, color=(0, 0, 0))
                y_priv += 10
    
    # Guardar PDF
    if generar_en_memoria:
        # Generar en memoria y retornar bytes
        pdf_bytes = doc.tobytes()
        doc.close()
        return pdf_bytes
    else:
        # Guardar en archivo
        doc.save(output_path)
        doc.close()
        return output_path

