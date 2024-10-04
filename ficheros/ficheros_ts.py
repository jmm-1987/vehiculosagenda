from flask import Flask, request, send_file
import openpyxl
import io
import pandas as pd

app = Flask(__name__)

# Registrar la función de subida y procesamiento de fichero
def register_func_subir_fichero_ts(app):
    @app.route("/subir_fichero_ts", methods=['POST'])
    def subir_fichero_ts():
        ficheros = request.files.getlist('fichero')
        if not ficheros:
            return "No se ha subido ningún archivo", 400

        # Leer el archivo Excel
        file = ficheros[0]  # Procesar solo el primer archivo en este caso
        excel_data = pd.ExcelFile(file)

        # Procesar la hoja de trabajo
        hoja = 'DISTRIBUCION'
        df = excel_data.parse(hoja)

        listas_expediciones = []
        datos_excel = []
        vacia = ""

        # Procesar el DataFrame y generar las listas de expediciones
        for index, row in df.iterrows():
            fila_lista = row.tolist()
            listas_expediciones.append(fila_lista)

        # Procesar las expediciones y formatear los datos
        for exp in listas_expediciones:
            if pd.isna(exp[0]):
                continue
            prefijoint = round(exp[0])
            prefijostr = str(prefijoint)
            if len(prefijostr) == 1 or len(prefijostr) == 2:
                prefijo = prefijostr + "1" + "-"
            elif len(prefijostr) == 3:
                prefijo = prefijostr + "-"
            expentera = str(exp[4])
            expsinpunto = expentera[:-2]
            expsolo9 = expsinpunto[-9:]
            limpia = expsolo9.lstrip('0')
            expedicion = prefijo + limpia

            fecha_entera = exp[5]
            formateada = fecha_entera.strftime('%d/%m/%Y')

            importe = round(exp[14], 2)

            # Añadir los datos a la lista final
            datos_excel.append(
                [formateada, expedicion, vacia, vacia, vacia, vacia, vacia, vacia, vacia, vacia, vacia, importe])

        # Crear un libro de trabajo de Excel en memoria
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "ImportacionXPO"
        ws.append(
            ["Fecha", "Expedición", "Vacia", "Vacia", "Vacia", "Vacia", "Vacia", "Vacia", "Vacia", "Vacia", "Vacia",
             "Importe"])

        # Escribir los datos procesados en la hoja de Excel
        for row in datos_excel:
            ws.append(row)

        # Guardar el archivo de Excel en memoria
        output = io.BytesIO()
        wb.save(output)
        output.seek(0)

        # Enviar el archivo al cliente
        return send_file(output, download_name="TSH_adaptado.xlsx", as_attachment=True)




