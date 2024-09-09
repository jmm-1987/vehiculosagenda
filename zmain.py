from flask import Flask, render_template, request, redirect, url_for
import db
from models import Tarea
from datetime import date, datetime, timedelta
from db import session


application = Flask(__name__)

@app.route('/')
def home():
    hoy = datetime.today().date()
    manana = hoy + timedelta(days=1)
    lista_hoy = db.session.query(Tarea).filter(Tarea.fecha_alerta == hoy).all()
    lista_proxima = db.session.query(Tarea).filter(Tarea.fecha_alerta >= manana).all()
    lista_proxima_ordenada = sorted(lista_proxima, key=lambda tarea: tarea.fecha_alerta)

    return render_template("index.html", lista_hoy = lista_hoy, lista_proxima = lista_proxima_ordenada, hoy=hoy)

@app.route('/pasadas')
def home_pasadas():
    hoy = datetime.today().date()
    lista_pasadas = db.session.query(Tarea).filter(Tarea.fecha_alerta < hoy).all()
    lista_pasadas_ordenada = sorted(lista_pasadas, key=lambda tarea: tarea.fecha_alerta)

    return render_template("index_pasadas.html", lista_pasadas = lista_pasadas_ordenada, hoy=hoy)


@app.route('/form_nueva_tarea')
def formulario_tarea():
    return render_template("form_nueva_tarea.html")

@app.route('/grabar_tarea', methods=["POST"])
def grabar_tarea():
    ffecha_alerta = request.form.get('fecha_alerta')
    tarea = Tarea(titulo=request.form["titulo"],
              contenido=request.form["contenido"],
              fecha_alta = date.today(),
              fecha_alerta = datetime.strptime(ffecha_alerta, '%d-%m-%Y'),
              realizada = False)

    db.session.add(tarea)
    db.session.commit()
    return redirect(url_for('home'))
@app.route('/borrar_tarea/<id>', methods=["POST", "GET"])
def borrar_tarea(id):
    registro_borrar = db.session.query(Tarea).filter_by(id=id).first()
    db.session.delete(registro_borrar)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/realizar_tarea/<id>', methods=["POST", "GET"])
def realizar_tarea(id):
    registro_realizar = db.session.query(Tarea).filter_by(id=id).first()
    registro_realizar.realizada = True
    usuario = request.form["usuario"]
    registro_realizar.usuario = usuario
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/anular_realizar_tarea/<id>', methods=["POST", "GET"])
def anular_realizar_tarea(id):
    registro_realizar = db.session.query(Tarea).filter_by(id=id).first()
    registro_realizar.realizada = False
    usuario = request.form.get('usuario')
    print(usuario)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/posponer/<tarea_id>', methods=['POST'])
def posponer(tarea_id):
    nueva_fecha = request.form.get('nueva_fecha')
    fecha_nueva = datetime.strptime(nueva_fecha, '%d-%m-%Y')
    registro_posponer = db.session.query(Tarea).filter_by(id=tarea_id).first()
    registro_posponer.fecha_alerta = fecha_nueva
    db.session.commit()
    return redirect(url_for('home'))




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    db.Base.metadata.create_all(db.engine)
    application.run()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
