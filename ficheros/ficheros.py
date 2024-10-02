from flask import Flask, request, send_file
import pandas as pd
import openpyxl
import io
from io import BytesIO

app = Flask(__name__)

# Registrar la función de subida y procesamiento de fichero
def register_func_subir_fichero(app):
    @app.route("/subir_fichero", methods=['POST'])
    def subir_fichero():
        ficheros = request.files.getlist('fichero')

        if not ficheros:
            return "No se ha subido ningún archivo", 400

        datos_excel = []

        for fichero in ficheros:
            # Leemos el contenido del archivo directamente usando read().
            contenido_bytes = fichero.read()  # Leer el contenido como bytes

            # Decodificar el contenido a texto usando 'mac_roman' o cualquier codificación necesaria
            try:
                contenido_texto = contenido_bytes.decode('mac_roman')
            except UnicodeDecodeError as e:
                return f"Error de codificación en el archivo {fichero.filename}: {e}"

            # Procesar el contenido en formato de texto
            listas_filas = contenido_texto.splitlines()  # Divide el texto en filas por líneas
            filas_procesadas = []

            for line in listas_filas:
                # Dividir la línea y eliminar espacios en blanco de cada elemento
                row = [element.strip() for element in line.split('","')]  # Eliminar espacios en blanco y comillas
                filas_procesadas.append(row)

                if len(row) in [49, 50, 51, 52]:  # Validar la longitud de las filas
                    row_converted = row[:17]
                    row_converted += [
                        float(element.replace(",", ".")) if element.replace('.', '', 1).replace('-', '',1).isdigit() else element
                        for element in row[17:]
                    ]
                    datos_excel.append(row_converted)


            # Crear un libro de trabajo de Excel
            wb = openpyxl.Workbook()
            ws = wb.active

            # Definir encabezados de columna
            ws.title = "ImportacionXPO"
            ws.append(["FACTURA", "FECHA FACTURA", "FECHA RECOGIDA", "DEPOT", "EXPEDICION", "PEDIDO", "REMITENTE",
                       "COD POSTAL", "ORIGEN", "VEHICULO", "TRAILER", "FECHA ENTR", "DESTINATARIO",
                       "CODIGO POS", "DESTINO", "REF ENTREGA", "MERCANCIA", "BULTO", "PESO", "VOLUMEN", "R100", "R83",
                       "R8", "T100", "T83", "D100", "D83", "D8", "D110", "D111", "D112", "D51",
                       "D70", "D75", "M1", "M100", "M2", "M3", "M17", "M40", "M99", "A14", "C1", "GASOIL", "SEGURO",
                       "SEGUN REC", "PARALIZACION", "OTROS", "TOTAL CS"])

            # Añadir los datos al archivo Excel
            for row in datos_excel:
                ws.append(row)

            # Guardar el archivo Excel
            output = io.BytesIO()
            wb.save(output)
            output.seek(0)

            # Enviar el archivo Excel como respuesta para descargar
            return send_file(output, download_name='imp_liq_XPO.xlsx')

        return "Archivos procesados correctamente"
