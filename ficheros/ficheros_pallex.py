from flask import Flask, request, send_file
import fitz
import re
import io
import openpyxl

app = Flask(__name__)

def register_func_subir_fichero_pallex(app):
    @app.route("/subir_fichero_pallex", methods=['POST'])
    def subir_fichero_pallex():
        file = request.files['fichero']
        if not file:
            return "No se ha subido ningún archivo", 400


        # Abrir el PDF usando PyMuPDF desde el stream
        doc = fitz.open(stream=file.read(), filetype="pdf")

        # Extraer el texto de todas las páginas
        full_text = ""
        for page in doc:
            full_text += page.get_text() + "\n"

        # Patrón para detectar bloques de envío
        pattern = re.compile(r"""
            (?P<envio>\d{5,})\s+              # número de envío
            \d{2}/\d{2}/\d{4}.*?              # fecha y texto intermedio
            (?P<total>\d+\.\d{2})\s+          # total
            0\.00\s+                          # valor fijo
            (?P=total)                        # el mismo total otra vez
        """, re.VERBOSE | re.DOTALL)

        # Extraer datos relevantes
        data = []
        for match in pattern.finditer(full_text):
            numero_envio = match.group("envio")
            total_precio = match.group("total")
            fila = ["", "", "", "", float(total_precio), "D", "", "", numero_envio]
            data.append(fila)

        # Crear un archivo Excel en memoria
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Importacion_costes_PALLEX"

        # Agregar encabezados
        ws.append(["Vacia", "Vacia", "Vacia", "Vacia", "Importe", "Clave", "Vacia", "Vacia", "Importe"])

        # Agregar filas de datos
        for fila in data:
            ws.append(fila)

        # Guardar el archivo en un buffer
        output = io.BytesIO()
        wb.save(output)
        output.seek(0)

        # Enviar archivo al cliente
        return send_file(output, download_name="ImportacionXPO.xlsx", as_attachment=True)
