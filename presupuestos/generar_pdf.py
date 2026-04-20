"""
Módulo para generar PDFs de presupuestos
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

# Observaciones del presupuesto
OBSERVACIONES_PRESUPUESTO = """VALIDEZ DEL PRESUPUESTO: 15 DÍAS DESDE SU COMUNICACIÓN:

MUY IMPORTANTE A TENER EN CUENTA PARA ACEPTACIÓN DE PRESUPUESTO
La mercancía debe estar perfectamente embalada, paletizada para ser transportada en nuestra red.

**Esta mercancía transportada no es cubierta por nuestro seguro. Con lo cual, cualquier avería o daño, pérdida que surja en estas tipologías o similares en caso de aceptación de servicio no serán admitidas sus reclamaciones por parte de Alditraex.

*No entramos en fincas, nuestras entregas y recogidas son puerta a puerta.-

"Si el bulto una vez recibido en nuestro almacén difiriera de las medidas y pesos que nos han dicho ustedes en la petición del servicio, deben saber que primaran las medidas y pesos tomadas en nuestras instalaciones para el precio del servicio a pagar."""


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
    
    # === INFORMACIÓN DEL CLIENTE (derecha) ===
    y_pos_cliente = 120  # Bajar más desde 100 a 120
    
    # === INFORMACIÓN DE LA EMPRESA (izquierda) - misma altura que CLIENTE ===
    y_pos = y_pos_cliente  # Misma altura que el bloque CLIENTE
    page.insert_text((50, y_pos), EMPRESA_NOMBRE, fontsize=font_size_header, color=(0, 0, 0))
    y_pos += 15
    page.insert_text((50, y_pos), EMPRESA_DIRECCION, fontsize=font_size_normal, color=(0, 0, 0))
    y_pos += 12
    page.insert_text((50, y_pos), EMPRESA_DIRECCION_2, fontsize=font_size_normal, color=(0, 0, 0))
    y_pos += 12
    page.insert_text((50, y_pos), f"CIF: {EMPRESA_CIF}", fontsize=font_size_normal, color=(0, 0, 0))
    page.insert_text((320, y_pos_cliente), "CLIENTE:", fontsize=font_size_normal, color=(0, 0, 0))
    y_pos_cliente += 12
    page.insert_text((320, y_pos_cliente), f"Nombre: {cliente.nombre}", fontsize=font_size_normal, color=(0, 0, 0))
    y_pos_cliente += 12
    page.insert_text((320, y_pos_cliente), f"Dirección: {cliente.direccion}", fontsize=font_size_normal, color=(0, 0, 0))
    y_pos_cliente += 12
    if cliente.poblacion:
        page.insert_text((320, y_pos_cliente), f"Población: {cliente.poblacion}", fontsize=font_size_normal, color=(0, 0, 0))
        y_pos_cliente += 12
    page.insert_text((320, y_pos_cliente), "Provincia:", fontsize=font_size_normal, color=(0, 0, 0))
    y_pos_cliente += 12
    page.insert_text((320, y_pos_cliente), f"CIF/NIF: {cliente.cif}", fontsize=font_size_normal, color=(0, 0, 0))
    y_pos_cliente += 12
    if cliente.email:
        page.insert_text((320, y_pos_cliente), f"Email: {cliente.email}", fontsize=font_size_normal, color=(0, 0, 0))
        y_pos_cliente += 12
    
    # === INFORMACIÓN DEL PRESUPUESTO (centrado, en negrita) ===
    y_pos_presupuesto = y_pos_cliente + 20
    fecha_str = presupuesto.fecha_presupuesto.strftime('%d/%m/%Y') if presupuesto.fecha_presupuesto else ""
    # Texto combinado: FECHA: dd/mm/aaaa Nº PRESUPUESTO: x
    texto_presupuesto = f"FECHA: {fecha_str}    Nº PRESUPUESTO: {presupuesto.numero_presupuesto}"
    
    # Calcular posición centrada (ancho del documento A4 = 595.2756 puntos)
    # Aproximación: fuente 12 tiene aproximadamente 0.6 puntos por carácter
    # Para fuente header (12), usar factor de 0.6
    ancho_texto = len(texto_presupuesto) * font_size_header * 0.5
    x_centrado = (595.2756 - ancho_texto) / 2
    
    # Insertar texto en negrita (usando tamaño de fuente mayor para simular negrita)
    # Usar la misma altura que tenía "PRESUPUESTO" (que estaba 24 puntos más abajo)
    y_pos_texto = y_pos_presupuesto + 24
    page.insert_text((x_centrado, y_pos_texto), texto_presupuesto, fontsize=font_size_header, color=(0, 0, 0))
    
    # === TABLA DE CONCEPTOS ===
    y_tabla = y_pos_texto + 30  # Espacio después del texto centrado
    
    # Encabezados de la tabla
    headers = ["N°", "OBSERVACIONES", "PRECIO", "% IVA", "IVA", "TOTAL"]
    # Columnas más estrechas: Precio, % IVA, IVA, Total; más espacio para Observaciones
    col_widths = [30, 330, 50, 35, 50, 55]
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
    
    # Observaciones con manejo de múltiples líneas
    observaciones_texto = presupuesto.observaciones if presupuesto.observaciones else ""
    ancho_col_observaciones = col_widths[1] - 10  # Ancho disponible menos márgenes
    y_obs_current = y_row
    
    # Función para dividir texto en líneas con máximo de caracteres
    def dividir_texto_en_lineas(texto, max_chars_por_linea=50):
        """Divide texto en líneas de hasta max_chars_por_linea, respetando palabras y saltos manuales."""
        if not texto:
            return []

        lineas = []
        parrafos = texto.replace('\r', '').split('\n')

        for parrafo in parrafos:
            palabras = [p for p in parrafo.split(' ') if p]
            if not palabras:
                lineas.append("")
                continue

            linea_actual = ""
            for palabra in palabras:
                test_linea = f"{linea_actual} {palabra}".strip() if linea_actual else palabra
                if len(test_linea) > max_chars_por_linea and linea_actual:
                    lineas.append(linea_actual)
                    linea_actual = palabra
                else:
                    linea_actual = test_linea

            if linea_actual:
                lineas.append(linea_actual)

        return lineas
    
    # Dividir observaciones en líneas y reservar siempre un mínimo de 3 líneas visibles
    lineas_observaciones = []
    if observaciones_texto:
        lineas_observaciones = dividir_texto_en_lineas(observaciones_texto, max_chars_por_linea=50)

    lineas_visibles_minimas = 3
    total_lineas_reservadas = max(len(lineas_observaciones), lineas_visibles_minimas)

    for i in range(total_lineas_reservadas):
        if i < len(lineas_observaciones):
            page.insert_text((x_positions[1] + 5, y_obs_current), lineas_observaciones[i], fontsize=font_size_normal, color=(0, 0, 0))
        y_obs_current += 13  # Espacio entre líneas (aumentado de 12 a 13)
    
    # Segunda sección: Bultos, Kg y Medidas (con espacio adicional para evitar solapamiento)
    y_row_2 = y_obs_current + 10  # Espacio adicional aumentado de 5 a 10 puntos para separar claramente
    bultos = presupuesto.bultos if presupuesto.bultos else "-"
    kg = presupuesto.kg if presupuesto.kg else "-"
    medidas = presupuesto.medidas if presupuesto.medidas else "-"
    detalle_texto = f"Bultos: {bultos}, Kg: {kg}, Medidas: {medidas}"
    
    # Dividir también el texto de detalles si es muy largo
    lineas_detalle = dividir_texto_en_lineas(detalle_texto, max_chars_por_linea=50)
    y_detalle_current = y_row_2
    for linea in lineas_detalle:
        page.insert_text((x_positions[1] + 5, y_detalle_current), linea, fontsize=font_size_small, color=(0, 0, 0))
        y_detalle_current += 10  # Espacio entre líneas de detalles
    
    # Calcular la altura máxima de la fila (observaciones o detalles)
    y_row_max = max(y_obs_current, y_detalle_current)
    
    # Precio (alineado con la primera línea de observaciones)
    precio_str = f"{presupuesto.importe:.2f}"
    page.insert_text((x_positions[2] + 5, y_row), precio_str, fontsize=font_size_normal, color=(0, 0, 0))
    
    # % IVA (alineado con la primera línea de observaciones)
    iva_percent_str = f"{iva_percent:.0f}"
    page.insert_text((x_positions[3] + 5, y_row), iva_percent_str, fontsize=font_size_normal, color=(0, 0, 0))
    
    # IVA (alineado con la primera línea de observaciones)
    iva_str = f"{presupuesto.iva:.2f}"
    page.insert_text((x_positions[4] + 5, y_row), iva_str, fontsize=font_size_normal, color=(0, 0, 0))
    
    # Total (alineado con la primera línea de observaciones)
    total_str = f"{presupuesto.total:.2f}"
    page.insert_text((x_positions[5] + 5, y_row), total_str, fontsize=font_size_normal, color=(0, 0, 0))
    
    # Línea debajo de la fila (ajustada dinámicamente según el contenido más largo)
    y_row_bottom = y_row_max + 10
    page.draw_line((x_start, y_row_bottom), (x_start + sum(col_widths), y_row_bottom), color=(0, 0, 0), width=1)
    
    # === OBSERVACIONES ===
    y_obs = y_row_bottom + 30
    page.insert_text((50, y_obs), "OBSERVACIONES:", fontsize=font_size_header, color=(0, 0, 0))
    y_obs += 20
    
    # Insertar observaciones del presupuesto (justificado, usando ancho completo)
    def insertar_texto_justificado(texto, x_start, x_end, y_start, fontsize):
        """Función auxiliar para insertar texto multilínea justificado"""
        # Reemplazar saltos de línea por espacios para procesamiento uniforme
        texto = texto.replace('\n', ' ')
        # Dividir por espacios y filtrar espacios vacíos
        words = [w for w in texto.split(' ') if w.strip()]
        current_line = ""
        y_current = y_start
        ancho_disponible = x_end - x_start
        
        for word in words:
            test_line = current_line + word + " " if current_line else word + " "
            # Estimar ancho del texto (aproximación: 0.5 puntos por carácter)
            ancho_test = len(test_line) * fontsize * 0.5
            
            if ancho_test > ancho_disponible and current_line:
                # Insertar línea actual
                page.insert_text((x_start, y_current), current_line.strip(), fontsize=fontsize, color=(0, 0, 0))
                y_current += fontsize + 2
                current_line = word + " "
            else:
                current_line = test_line
        
        # Insertar última línea
        if current_line.strip():
            page.insert_text((x_start, y_current), current_line.strip(), fontsize=fontsize, color=(0, 0, 0))
            y_current += fontsize + 2
        
        return y_current
    
    # Usar ancho completo del documento para justificar mejor (márgenes de 50 a cada lado)
    x_start_texto = 50
    x_end_texto = 545  # 595.2756 - 50 (margen derecho)
    
    obs_lines = OBSERVACIONES_PRESUPUESTO.split('\n')
    for line in obs_lines:
        if line.strip():
            y_obs = insertar_texto_justificado(line.strip(), x_start_texto, x_end_texto, y_obs, font_size_small)
            y_obs += 5  # Espacio entre párrafos
    
    # === RECUADRO DE TRANSFERENCIA ===
    y_obs += 25  # Separar más del resto
    texto_transferencia = "En el caso de estar de acuerdo con la cotización ofrecida, rogamos hagan el ingreso por transferencia a la cuenta nº "
    numero_cuenta = "ES38 0078 0076 4440 0000 3347 "
    texto_transferencia_fin = "  (adjunten copia de la misma a este email) para poder poner en marcha el servicio."
    
    # Dimensiones del recuadro
    x_recuadro = 50
    ancho_recuadro = 495  # 545 - 50
    ancho_texto_disponible = ancho_recuadro - 20  # Margen de 10 a cada lado
    font_size_recuadro = font_size_small + 1
    
    # Calcular altura necesaria para el texto (aproximadamente 2-3 líneas)
    alto_recuadro = 60
    y_recuadro_top = y_obs
    y_recuadro_bottom = y_obs + alto_recuadro
    
    # Dibujar recuadro
    box_rect = fitz.Rect(x_recuadro, y_recuadro_top, x_recuadro + ancho_recuadro, y_recuadro_bottom)
    page.draw_rect(box_rect, color=(0, 0, 0), width=1)
    
    # Insertar texto dentro del recuadro usando función multilínea
    y_texto_recuadro = y_recuadro_top + 15
    x_texto_inicio = x_recuadro + 10
    
    # Construir texto completo con número de cuenta destacado
    # Primera línea: texto hasta el número de cuenta
    texto_completo = texto_transferencia + numero_cuenta + texto_transferencia_fin
    
    # Insertar texto con manejo de múltiples líneas y número de cuenta en negrita
    # Dividir el texto en partes: antes del número, número, después del número
    partes = texto_completo.split(numero_cuenta)
    
    if len(partes) == 2:
        # Primera parte (antes del número de cuenta)
        texto_antes = partes[0].strip()
        texto_despues = partes[1].strip()
        
        # Insertar texto completo línea por línea, insertando el número de cuenta en la misma línea cuando corresponda
        words_antes = texto_antes.split(' ')
        words_despues = texto_despues.split(' ')
        all_words = words_antes + [numero_cuenta] + words_despues
        
        current_line = ""
        y_current = y_texto_recuadro
        x_current = x_texto_inicio
        encontrado_numero = False
        
        for word in all_words:
            # Verificar si esta palabra es el número de cuenta
            es_numero_cuenta = word == numero_cuenta
            
            test_line = current_line + word + " " if current_line else word + " "
            ancho_test = len(test_line) * font_size_recuadro * 0.5
            
            if ancho_test > ancho_texto_disponible and current_line:
                # Insertar línea actual
                if numero_cuenta in current_line and not encontrado_numero:
                    # Dividir la línea para insertar el número de cuenta en negrita
                    partes_linea = current_line.split(numero_cuenta)
                    if len(partes_linea) == 2:
                        # Insertar parte antes del número
                        if partes_linea[0].strip():
                            page.insert_text((x_current, y_current), partes_linea[0].strip(), fontsize=font_size_recuadro, color=(0, 0, 0))
                            ancho_antes = len(partes_linea[0].strip()) * font_size_recuadro * 0.5
                            x_cuenta = x_current + ancho_antes
                        else:
                            x_cuenta = x_current
                        # Insertar número de cuenta (mismo tamaño, pero en negrita visual con fuente más grande ligeramente)
                        page.insert_text((x_cuenta, y_current), numero_cuenta, fontsize=font_size_recuadro, color=(0, 0, 0))
                        ancho_cuenta = len(numero_cuenta) * font_size_recuadro * 0.5
                        # Insertar parte después del número
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
        
        # Insertar última línea
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
        
        # Ajustar altura del recuadro
        y_final_recuadro = y_current
        if y_final_recuadro > y_recuadro_bottom - 5:
            nuevo_alto = y_final_recuadro - y_recuadro_top + 10
            box_rect = fitz.Rect(x_recuadro, y_recuadro_top, x_recuadro + ancho_recuadro, y_recuadro_top + nuevo_alto)
            page.draw_rect(box_rect, color=(0, 0, 0), width=1)
            y_recuadro_bottom = y_recuadro_top + nuevo_alto
        else:
            y_recuadro_bottom = y_final_recuadro + 5
    else:
        # Si no se encuentra el número, insertar texto normal
        y_final = insertar_texto_justificado(texto_completo, x_texto_inicio, x_recuadro + ancho_recuadro - 10, y_texto_recuadro, font_size_recuadro)
        # Ajustar altura del recuadro
        if y_final > y_recuadro_bottom - 5:
            nuevo_alto = y_final - y_recuadro_top + 10
            box_rect = fitz.Rect(x_recuadro, y_recuadro_top, x_recuadro + ancho_recuadro, y_recuadro_top + nuevo_alto)
            page.draw_rect(box_rect, color=(0, 0, 0), width=1)
            y_recuadro_bottom = y_recuadro_top + nuevo_alto
        else:
            y_recuadro_bottom = y_final + 5
    
    # === POLÍTICA DE PRIVACIDAD (al pie del documento) ===
    texto_privacidad = """Política de privacidad. Sus datos personales serán usados para nuestra relación y poder prestarle nuestros servicios. Dichos datos
son necesarios para poder relacionarnos con usted, lo que nos permite el uso de su información dentro de la legalidad. Asimismo,
podrán tener conocimiento de su información aquellas entidades que necesiten tener acceso a la misma para que podamos
prestarle nuestros servicios. Conservaremos sus datos durante nuestra relación y mientras nos obliguen las leyes aplicables. En
cualquier momento puede dirigirse a nosotros para saber qué información tenemos sobre usted, rectificarla si fuese incorrecta y
eliminarla una vez finalizada nuestra relación. También tiene derecho a solicitar el traspaso de su información a otra entidad
(portabilidad). Para solicitar alguno de estos derechos, deberá realizar una solicitud escrita a nuestra dirección, junto con una
fotocopia de su DNI: ---- CP 06800, Mérida (Badajoz). En caso de que entienda que sus derechos han sido desatendidos, puede
formular una reclamación en la Agencia Española de Protección de Datos (www.agpd.es)."""
    
    # Insertar texto justificado después del recuadro con más espacio para evitar solapamiento
    y_privacidad = y_recuadro_bottom + 30  # Espacio aumentado de 15 a 30 puntos para evitar solapamiento
    font_size_privacidad = 7
    
    # Insertar texto justificado con márgenes laterales (50 a 545) y capturar posición final
    y_final_privacidad = insertar_texto_justificado(texto_privacidad, 50, 545, y_privacidad, font_size_privacidad)
    
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

