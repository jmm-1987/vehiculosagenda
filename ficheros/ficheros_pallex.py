from flask import Flask, request, send_file
import fitz
import re
import io
import openpyxl
from openpyxl.styles import numbers

app = Flask(__name__)

def register_func_subir_fichero_pallex(app):
    @app.route("/subir_fichero_pallex", methods=['POST'])
    def subir_fichero_pallex():
        file = request.files['fichero']
        if not file:
            return "No se ha subido ningún archivo", 400

        # Abrir el PDF usando PyMuPDF desde el stream
        doc = fitz.open(stream=file.read(), filetype="pdf")

        # Reconstruir correctamente los números de expedición partidos por salto de línea
        text_lines = []
        for page in doc:
            lines = page.get_text("text").splitlines()
            i = 0
            while i < len(lines):
                line = lines[i].strip()
                if line.endswith("_") and (i + 1 < len(lines)):
                    # Unir línea que termina en "_" con la siguiente línea
                    next_line = lines[i + 1].strip()
                    combined = line + next_line
                    text_lines.append(combined)
                    i += 2  # Saltar la siguiente línea porque ya la hemos unido
                else:
                    text_lines.append(line)
                    i += 1

        # Convertir a texto plano
        full_text = " ".join(text_lines)

        # Expresión regular para detectar el número de envío, fecha, e importe
        pattern = re.compile(r"""
            (?P<envio>[A-Za-z0-9_\-]+?)\s+          # Número de expedición
            \d{2}/\d{2}/\d{4}.*?                    # Fecha y texto intermedio
            (?P<total>\d+\.\d{2})\s+                # Importe total
            0\.00\s+                                # Cargos
            (?P=total)                              # Total final igual al importe
        """, re.VERBOSE | re.DOTALL)

        # Extraer datos relevantes
        data = []
        for match in pattern.finditer(full_text):
            numero_envio = match.group("envio")
            total_precio = match.group("total")
            fila = ["", "", "", "", float(total_precio), "D", "", "", str(numero_envio)]
            data.append(fila)

        # Crear Excel
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Importacion_costes_PALLEX"
        ws.append(["Vacia", "Vacia", "Vacia", "Vacia", "Importe", "Clave", "Vacia", "Vacia", "Importe"])

        for fila in data:
            ws.append(fila)
            ws.cell(row=ws.max_row, column=9).number_format = numbers.FORMAT_TEXT

        # Guardar el archivo en un buffer
        output = io.BytesIO()
        wb.save(output)
        output.seek(0)

        # Enviar archivo al cliente
        return send_file(output, download_name="Imp_costes_PALLEX.xlsx", as_attachment=True)
