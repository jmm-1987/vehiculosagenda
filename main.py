from flask import Flask, render_template, session, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
import db
from models import Itv, Seguro, Tacografo, Rodaje, Extintor, Usuario
from datetime import datetime, timedelta
from vehiculos.vehiculos import register_vehiculos_routes
from itv.itv import register_itv_routes
from seguros.seguros import register_seguros_routes
from tacografos.tacografos import register_tacografos_routes
from rodajes.rodajes import register_rodajes_routes
from extintores.extintores import register_extintores_routes
from tickets.tickets import register_tickets_routes
from tickets.funciones_ticket import register_funciones_tickets_routes
from itv.edicion import register_itvedit_routes
from func_especiales.funciones import register_func_especiales_routes
from vehiculos.ficha_vehiculos import register_ficha_routes
from seguros.edicion import register_seguroedit_routes
from tacografos.edicion import register_tacografoedit_routes
from rodajes.edicion import register_rodajeedit_routes
from extintores.edicion import register_extintoredit_routes
from manager.manager import register_usuarios_routes
from transpaletas.transpaletas import register_transpaletas_routes
from transpaletas.ficha_transpaleta import register_transpaleta_talleres_routes
from transpaletas.visitas_transpaleta import register_visitas_transapaleta_routes
from talleres.talleres import register_talleres_routes
from talleres.edicion import register_talleredit_routes
from tareas.tareas import register_tareas_routes
from ficheros.ficheros import register_func_subir_fichero

#Arranque app
app = Flask(__name__)
app.config['SECRET_KEY'] = '78587fgrtyth'

#instancia del logi
login_manager = LoginManager(app)

#Esto es de login
#login_manager = LoginManager(app)

#Configuracion del sitio de las imagenes
app.config['UPLOAD_FOLDER'] = 'static/subidas'

#Rutas
register_vehiculos_routes(app)
register_itv_routes(app)
register_seguros_routes(app)
register_tacografos_routes(app)
register_rodajes_routes(app)
register_extintores_routes(app)
register_tickets_routes(app)
register_itvedit_routes(app)
register_func_especiales_routes(app)
register_ficha_routes(app)
register_funciones_tickets_routes(app)
register_seguroedit_routes(app)
register_tacografoedit_routes(app)
register_rodajeedit_routes(app)
register_extintoredit_routes(app)
register_usuarios_routes(app)
register_transpaletas_routes(app)
register_transpaleta_talleres_routes(app)
register_visitas_transapaleta_routes(app)
register_talleres_routes(app)
register_talleredit_routes(app)
register_tareas_routes(app)
register_func_subir_fichero(app)

@app.route('/')
def index():
    return redirect(url_for('login'))

@login_manager.user_loader
def load_user(user_id):
    return db.session.query(Usuario).filter_by(id=user_id).first()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        usuario = db.session.query(Usuario).filter_by(username=username).first()
        if usuario and usuario.password == password:
            login_user(usuario)
            return redirect(url_for('home'))
        else:
            return render_template('login.html', mensaje="Usuario o contraseña incorrectos")
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/index')
@login_required
def home():
    avisos = []
    ahora = datetime.now().date()
    referencia = ahora + timedelta(days=30)
    todas_itv = db.session.query(Itv).all()
    todos_seguros = db.session.query(Seguro).all()
    todos_tacografos = db.session.query(Tacografo).all()
    todos_rodajes = db.session.query(Rodaje).all()
    todos_extintores = db.session.query(Extintor).all()
    for v in todas_itv:
        temporal = v.venc_itv
        if temporal.date() < referencia:
            avisos_itv = []
            avisos_itv.append(temporal.date().strftime("%d-%m-%Y"))
            avisos_itv.append(v.matricula)
            avisos_itv.append("caduda la ITV")
            avisos.append(avisos_itv)
    for v in todos_seguros:
        temporal = v.venc_seguro
        if temporal.date() < referencia:
            avisos_seguros = []
            avisos_seguros.append(temporal.date().strftime("%d-%m-%Y"))
            avisos_seguros.append(v.matricula)
            avisos_seguros.append("vence el seguro")
            avisos.append(avisos_seguros)
    for v in todos_tacografos:
        temporal = v.venc_tacografo
        if temporal.date() < referencia:
            avisos_tacografos = []
            avisos_tacografos.append(temporal.date().strftime("%d-%m-%Y"))
            avisos_tacografos.append(v.matricula)
            avisos_tacografos.append("caduca el tacógrafo")
            avisos.append(avisos_tacografos)
    for v in todos_rodajes:
        temporal = v.venc_rodaje
        if temporal.date() < referencia:
            avisos_rodajes = []
            avisos_rodajes.append(temporal.date().strftime("%d-%m-%Y"))
            avisos_rodajes.append(v.matricula)
            avisos_rodajes.append("renovacion del rodaje")
            avisos.append(avisos_rodajes)
    for v in todos_extintores:
        temporal = v.venc_ext
        if temporal.date() < referencia:
            avisos_extintores = []
            avisos_extintores.append(temporal.date().strftime("%d-%m-%Y"))
            avisos_extintores.append(v.matricula)
            avisos_extintores.append("caducidad extintores")
            avisos.append(avisos_extintores)

    avisos = sorted(avisos, key=lambda x: x[0])

    return render_template('index.html', avisos=avisos)


if __name__ == '__main__':
    db.Base.metadata.create_all(db.engine)
    app.run(debug=True)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
