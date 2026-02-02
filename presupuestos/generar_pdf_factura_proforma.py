"""
Módulo para generar PDFs de facturas proforma
"""
import os
import fitz  # PyMuPDF
from datetime import datetime

# Datos de la empresa
EMPRESA_NOMBRE = "Alditraex SL"
EMPRESA_DIRECCION = "C/Cadiz, 15 Pol Ind El Prado"
EMPRESA_DIRECCION_2 = "06800-Mérida (Badajoz)"
EMPRESA_CIF = "B06422208"
EMPRESA_CUENTA_BANCARIA = "ES38 0078 0076 4440 0000 3347"


def generar_pdf_factura_proforma(factura_proforma, presupuesto, cliente, output_path=None):
    """
    Genera un PDF de la factura proforma con el formato especificado.
    Similar al presupuesto pero indicando que es FACTURA PROFORMA y haciendo referencia al presupuesto.
    
    Args:
        factura_proforma: Objeto FacturaProforma
        presupuesto: Objeto Presupuesto (referencia)
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
            img_rect = fitz.Rect(50, 30, 200, 80)
            page.insert_image(img_rect, filename=logo_path)
        except Exception as e:
            print(f"Error al insertar logo: {e}")
    
    # === INFORMACIÓN DEL CLIENTE (derecha) ===
    y_pos_cliente = 120
    
    # === INFORMACIÓN DE LA EMPRESA (izquierda) ===
    y_pos = y_pos_cliente
    page.insert_text((50, y_pos), EMPRESA_NOMBRE, fontsize=font_size_header, color=(0, 0, 0))
    y_pos += 15
    page.insert_text((50, y_pos), EMPRESA_DIRECCION, fontsize=font_size_normal, color=(0, 0, 0))
    y_pos += 12
    page.insert_text((50, y_pos), EMPRESA_DIRECCION_2, fontsize=font_size_normal, color=(0, 0, 0))
    y_pos += 12
    page.insert_text((50, y_pos), f"CIF: {EMPRESA_CIF}", fontsize=font_size_normal, color=(0, 0, 0))
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
    
    # === TÍTULO: FACTURA PROFORMA (centrado, en negrita) ===
    y_pos_titulo = y_pos_cliente + 20
    texto_titulo = "FACTURA PROFORMA"
    ancho_texto_titulo = len(texto_titulo) * font_size_title * 0.5
    x_centrado_titulo = (595.2756 - ancho_texto_titulo) / 2
    page.insert_text((x_centrado_titulo, y_pos_titulo), texto_titulo, fontsize=font_size_title, color=(0, 0, 0))
    
    # === INFORMACIÓN DE LA FACTURA PROFORMA Y REFERENCIA AL PRESUPUESTO ===
    y_pos_info = y_pos_titulo + 25
    fecha_str = factura_proforma.fecha_factura_proforma.strftime('%d/%m/%Y') if factura_proforma.fecha_factura_proforma else ""
    texto_info = f"FECHA: {fecha_str}    Nº FACTURA PROFORMA: {factura_proforma.numero_factura_proforma}"
    texto_referencia = f"REFERENCIA PRESUPUESTO: {presupuesto.numero_presupuesto}"
    
    # Calcular posición centrada
    ancho_texto_info = len(texto_info) * font_size_header * 0.5
    x_centrado_info = (595.2756 - ancho_texto_info) / 2
    page.insert_text((x_centrado_info, y_pos_info), texto_info, fontsize=font_size_header, color=(0, 0, 0))
    
    # Referencia al presupuesto (línea siguiente)
    y_pos_info += 18
    ancho_texto_ref = len(texto_referencia) * font_size_normal * 0.5
    x_centrado_ref = (595.2756 - ancho_texto_ref) / 2
    page.insert_text((x_centrado_ref, y_pos_info), texto_referencia, fontsize=font_size_normal, color=(0, 0, 0))
    
    # === TABLA DE CONCEPTOS ===
    y_tabla = y_pos_info + 30
    
    # Encabezados de la tabla
    headers = ["N°", "OBSERVACIONES", "PRECIO", "% IVA", "IVA", "TOTAL"]
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
    if factura_proforma.importe and factura_proforma.importe > 0:
        iva_percent = (factura_proforma.iva / factura_proforma.importe) * 100
    
    # Fila de datos
    y_row = y_header + 20
    page.insert_text((x_positions[0] + 5, y_row), "1", fontsize=font_size_normal, color=(0, 0, 0))
    
    # Observaciones con manejo de múltiples líneas
    observaciones_texto = factura_proforma.observaciones if factura_proforma.observaciones else ""
    ancho_col_observaciones = col_widths[1] - 10
    y_obs_current = y_row
    
    # Función para dividir texto en líneas según ancho disponible
    def dividir_texto_en_lineas(texto, ancho_maximo, fontsize):
        """Divide texto en líneas que caben en el ancho máximo"""
        palabras = texto.split(' ')
        lineas = []
        linea_actual = ""
        
        for palabra in palabras:
            test_linea = linea_actual + " " + palabra if linea_actual else palabra
            ancho_test = len(test_linea) * fontsize * 0.5
            
            if ancho_test > ancho_maximo and linea_actual:
                lineas.append(linea_actual)
                linea_actual = palabra
            else:
                linea_actual = test_linea
        
        if linea_actual:
            lineas.append(linea_actual)
        
        return lineas
    
    # Dividir observaciones en líneas si es necesario
    if observaciones_texto:
        lineas_observaciones = dividir_texto_en_lineas(observaciones_texto, ancho_col_observaciones, font_size_normal)
        for i, linea in enumerate(lineas_observaciones):
            page.insert_text((x_positions[1] + 5, y_obs_current), linea, fontsize=font_size_normal, color=(0, 0, 0))
            y_obs_current += 13
    else:
        y_obs_current += 13
    
    # Segunda sección: Bultos, Kg y Medidas
    y_row_2 = y_obs_current + 10
    bultos = factura_proforma.bultos if factura_proforma.bultos else "-"
    kg = factura_proforma.kg if factura_proforma.kg else "-"
    medidas = factura_proforma.medidas if factura_proforma.medidas else "-"
    detalle_texto = f"Bultos: {bultos}, Kg: {kg}, Medidas: {medidas}"
    
    lineas_detalle = dividir_texto_en_lineas(detalle_texto, ancho_col_observaciones, font_size_small)
    y_detalle_current = y_row_2
    for linea in lineas_detalle:
        page.insert_text((x_positions[1] + 5, y_detalle_current), linea, fontsize=font_size_small, color=(0, 0, 0))
        y_detalle_current += 10
    
    # Calcular la altura máxima de la fila
    y_row_max = max(y_obs_current, y_detalle_current)
    
    # Precio, % IVA, IVA y Total (alineados con la primera línea de observaciones)
    precio_str = f"{factura_proforma.importe:.2f}"
    page.insert_text((x_positions[2] + 5, y_row), precio_str, fontsize=font_size_normal, color=(0, 0, 0))
    
    iva_percent_str = f"{iva_percent:.0f}"
    page.insert_text((x_positions[3] + 5, y_row), iva_percent_str, fontsize=font_size_normal, color=(0, 0, 0))
    
    iva_str = f"{factura_proforma.iva:.2f}"
    page.insert_text((x_positions[4] + 5, y_row), iva_str, fontsize=font_size_normal, color=(0, 0, 0))
    
    total_str = f"{factura_proforma.total:.2f}"
    page.insert_text((x_positions[5] + 5, y_row), total_str, fontsize=font_size_normal, color=(0, 0, 0))
    
    # Línea debajo de la fila
    y_row_bottom = y_row_max + 10
    page.draw_line((x_start, y_row_bottom), (x_start + sum(col_widths), y_row_bottom), color=(0, 0, 0), width=1)
    
    # === OBSERVACIONES ===
    y_obs = y_row_bottom + 30
    page.insert_text((50, y_obs), "OBSERVACIONES:", fontsize=font_size_header, color=(0, 0, 0))
    y_obs += 20
    
    # Insertar texto justificado
    def insertar_texto_justificado(texto, x_start, x_end, y_start, fontsize):
        """Función auxiliar para insertar texto multilínea justificado"""
        texto = texto.replace('\n', ' ')
        words = [w for w in texto.split(' ') if w.strip()]
        current_line = ""
        y_current = y_start
        ancho_disponible = x_end - x_start
        
        for word in words:
            test_line = current_line + word + " " if current_line else word + " "
            ancho_test = len(test_line) * fontsize * 0.5
            
            if ancho_test > ancho_disponible and current_line:
                page.insert_text((x_start, y_current), current_line.strip(), fontsize=fontsize, color=(0, 0, 0))
                y_current += fontsize + 2
                current_line = word + " "
            else:
                current_line = test_line
        
        if current_line.strip():
            page.insert_text((x_start, y_current), current_line.strip(), fontsize=fontsize, color=(0, 0, 0))
            y_current += fontsize + 2
        
        return y_current
    
    x_start_texto = 50
    x_end_texto = 545
    
    # Texto específico para factura proforma
    texto_observaciones = f"Esta factura proforma hace referencia al presupuesto Nº {presupuesto.numero_presupuesto} con fecha {presupuesto.fecha_presupuesto.strftime('%d/%m/%Y') if presupuesto.fecha_presupuesto else ''}."
    
    y_obs = insertar_texto_justificado(texto_observaciones, x_start_texto, x_end_texto, y_obs, font_size_small)
    y_obs += 10
    
    # === RECUADRO DE TRANSFERENCIA ===
    y_obs += 25
    texto_transferencia = "En el caso de estar de acuerdo con la cotización ofrecida, rogamos hagan el ingreso por transferencia a la cuenta nº "
    numero_cuenta = "ES38 0078 0076 4440 0000 3347 "
    texto_transferencia_fin = "  (adjunten copia de la misma a este email) para poder poner en marcha el servicio."
    
    x_recuadro = 50
    ancho_recuadro = 495
    ancho_texto_disponible = ancho_recuadro - 20
    font_size_recuadro = font_size_small + 1
    
    alto_recuadro = 60
    y_recuadro_top = y_obs
    y_recuadro_bottom = y_obs + alto_recuadro
    
    # Dibujar recuadro
    box_rect = fitz.Rect(x_recuadro, y_recuadro_top, x_recuadro + ancho_recuadro, y_recuadro_bottom)
    page.draw_rect(box_rect, color=(0, 0, 0), width=1)
    
    # Insertar texto dentro del recuadro
    y_texto_recuadro = y_recuadro_top + 15
    x_texto_inicio = x_recuadro + 10
    
    texto_completo = texto_transferencia + numero_cuenta + texto_transferencia_fin
    partes = texto_completo.split(numero_cuenta)
    
    if len(partes) == 2:
        texto_antes = partes[0].strip()
        texto_despues = partes[1].strip()
        all_words = texto_antes.split(' ') + [numero_cuenta] + texto_despues.split(' ')
        
        current_line = ""
        y_current = y_texto_recuadro
        x_current = x_texto_inicio
        encontrado_numero = False
        
        for word in all_words:
            es_numero_cuenta = word == numero_cuenta
            test_line = current_line + word + " " if current_line else word + " "
            ancho_test = len(test_line) * font_size_recuadro * 0.5
            
            if ancho_test > ancho_texto_disponible and current_line:
                if numero_cuenta in current_line and not encontrado_numero:
                    partes_linea = current_line.split(numero_cuenta)
                    if len(partes_linea) == 2:
                        if partes_linea[0].strip():
                            page.insert_text((x_current, y_current), partes_linea[0].strip(), fontsize=font_size_recuadro, color=(0, 0, 0))
                            ancho_antes = len(partes_linea[0].strip()) * font_size_recuadro * 0.5
                            x_cuenta = x_current + ancho_antes
                        else:
                            x_cuenta = x_current
                        page.insert_text((x_cuenta, y_current), numero_cuenta, fontsize=font_size_recuadro, color=(0, 0, 0))
                        ancho_cuenta = len(numero_cuenta) * font_size_recuadro * 0.5
                        if partes_linea[1].strip():
                            page.insert_text((x_cuenta + ancho_cuenta, y_current), partes_linea[1].strip(), fontsize=font_size_recuadro, color=(0, 0, 0))
                        encontrado_numero = True
                    else:
                        page.insert_text((x_current, y_current), current_line.strip(), fontsize=font_size_recuadro, color=(0, 0, 0))
                else:
                    page.insert_text((x_current, y_current), current_line.strip(), fontsize=font_size_recuadro, color=(0, 0, 0))
                y_current += font_size_recuadro + 2
                current_line = word + " "
            else:
                current_line = test_line
        
        if current_line.strip():
            if numero_cuenta in current_line and not encontrado_numero:
                partes_linea = current_line.split(numero_cuenta)
                if len(partes_linea) == 2:
                    if partes_linea[0].strip():
                        page.insert_text((x_current, y_current), partes_linea[0].strip(), fontsize=font_size_recuadro, color=(0, 0, 0))
                        ancho_antes = len(partes_linea[0].strip()) * font_size_recuadro * 0.5
                        x_cuenta = x_current + ancho_antes
                    else:
                        x_cuenta = x_current
                    page.insert_text((x_cuenta, y_current), numero_cuenta, fontsize=font_size_recuadro, color=(0, 0, 0))
                    ancho_cuenta = len(numero_cuenta) * font_size_recuadro * 0.5
                    if partes_linea[1].strip():
                        page.insert_text((x_cuenta + ancho_cuenta, y_current), partes_linea[1].strip(), fontsize=font_size_recuadro, color=(0, 0, 0))
                else:
                    page.insert_text((x_current, y_current), current_line.strip(), fontsize=font_size_recuadro, color=(0, 0, 0))
            else:
                page.insert_text((x_current, y_current), current_line.strip(), fontsize=font_size_recuadro, color=(0, 0, 0))
            y_current += font_size_recuadro + 2
        
        y_final_recuadro = y_current
        if y_final_recuadro > y_recuadro_bottom - 5:
            nuevo_alto = y_final_recuadro - y_recuadro_top + 10
            box_rect = fitz.Rect(x_recuadro, y_recuadro_top, x_recuadro + ancho_recuadro, y_recuadro_top + nuevo_alto)
            page.draw_rect(box_rect, color=(0, 0, 0), width=1)
            y_recuadro_bottom = y_recuadro_top + nuevo_alto
        else:
            y_recuadro_bottom = y_final_recuadro + 5
    
    # === POLÍTICA DE PRIVACIDAD ===
    texto_privacidad = """Política de privacidad. Sus datos personales serán usados para nuestra relación y poder prestarle nuestros servicios. Dichos datos
son necesarios para poder relacionarnos con usted, lo que nos permite el uso de su información dentro de la legalidad. Asimismo,
podrán tener conocimiento de su información aquellas entidades que necesiten tener acceso a la misma para que podamos
prestarle nuestros servicios. Conservaremos sus datos durante nuestra relación y mientras nos obliguen las leyes aplicables. En
cualquier momento puede dirigirse a nosotros para saber qué información tenemos sobre usted, rectificarla si fuese incorrecta y
eliminarla una vez finalizada nuestra relación. También tiene derecho a solicitar el traspaso de su información a otra entidad
(portabilidad). Para solicitar alguno de estos derechos, deberá realizar una solicitud escrita a nuestra dirección, junto con una
fotocopia de su DNI: ---- CP 06800, Mérida (Badajoz). En caso de que entienda que sus derechos han sido desatendidos, puede
formular una reclamación en la Agencia Española de Protección de Datos (www.agpd.es)."""
    
    y_privacidad = y_recuadro_bottom + 30
    font_size_privacidad = 7
    
    y_final_privacidad = insertar_texto_justificado(texto_privacidad, 50, 545, y_privacidad, font_size_privacidad)
    
    # Guardar PDF
    if generar_en_memoria:
        pdf_bytes = doc.tobytes()
        doc.close()
        return pdf_bytes
    else:
        doc.save(output_path)
        doc.close()
        return output_path
