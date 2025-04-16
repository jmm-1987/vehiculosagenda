from flask import Flask, request, send_file
import openpyxl
import io

app = Flask(__name__)

def register_func_subir_fichero_xpo(app):
    @app.route("/subir_fichero_xpo", methods=['POST'])
    def subir_fichero_xpo():
        ficheros = request.files.getlist('fichero')
        if not ficheros:
            return "No se ha subido ningún archivo", 400

        datos_excel = []

        def safe_float(val):
            try:
                return float(val.strip('\"'))
            except:
                return 0.0

        for file in ficheros:
            content = file.read().decode('mac_roman').splitlines()
            listas_filas = []

            for line in content:
                row = line.strip().split('","')
                if len(row) in [49, 50, 51, 52]:
                    listas_filas.append(row)

            for i in listas_filas[1:]:
                expedicion = i[4].strip('\"').rstrip()

                r100 = safe_float(i[20])
                if r100:
                    datos_excel.append(["", "", "", r100, "r100", "", "", expedicion])
                r83 = safe_float(i[21])
                if r83:
                    datos_excel.append(["", "", "", r83, "r83", "", "", expedicion])
                r8 = safe_float(i[22])
                if r8:
                    datos_excel.append(["", "", "", r8, "r8", "", "", expedicion])

                t = round(safe_float(i[23]) + safe_float(i[24]), 2)
                if t:
                    datos_excel.append(["", "", "", t, "T", "", "", expedicion])

                d = round(safe_float(i[25]) + safe_float(i[26]), 2)
                if d:
                    datos_excel.append(["", "", "", d, "D", "", "", expedicion])

                d8 = safe_float(i[27])
                if d8:
                    datos_excel.append(["", "", "", d8, "D", "", "", expedicion])

                d9 = round(sum(map(safe_float, i[28:34])), 2)
                if d9:
                    datos_excel.append(["", "", "", d9, "D", "", "", expedicion])

                m = round(sum(map(safe_float, i[34:41])), 2)
                if m:
                    datos_excel.append(["", "", "", m, "M", "", "", expedicion])

                a = safe_float(i[41])
                if a:
                    datos_excel.append(["", "", "", a, "A", "", "", expedicion])

                c1 = safe_float(i[42])
                if c1:
                    datos_excel.append(["", "", "", c1, "D", "", "", expedicion])

                v = round(sum(map(safe_float, i[43:47])), 2)
                if v:
                    datos_excel.append(["", "", "", v, "V", "", "", expedicion])

        # Crear Excel en memoria
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "ImportacionXPO"
        ws.append(["Vacia", "Vacia", "Vacia", "Vacia", "Importe", "Clave", "Vacia", "Vacia", "Importe"])

        for row in datos_excel:
            ws.append(row)

        output = io.BytesIO()
        wb.save(output)
        output.seek(0)

        return send_file(output, download_name="imp_liq_XPO.xlsx", as_attachment=True)
