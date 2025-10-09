# Copia temporal de main.py SIN SSL para pruebas rápidas
# Nota: La cámara puede no funcionar en algunos navegadores móviles sin HTTPS

from flask import Flask, render_template, session, request, redirect, url_for, send_file
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
import db
from ftp_transfer.ftp_transfer import register_ftp_transfer_routes, iniciar_scheduler
from models import Itv, Seguro, Tacografo, Rodaje, Extintor, Usuario, Vehiculo, Taller
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
from ficheros.ficheros_ts import register_func_subir_fichero_ts
from ficheros.ficheros_pallex import register_func_subir_fichero_pallex
from ficheros.ficheros_xpo import register_func_subir_fichero_xpo
from ficheros.ficheros_carreras import register_func_subir_fichero_carreras
from scanner_ftp.scanner_ftp import register_scanner_ftp_routes
from sqlalchemy import func

iniciar_scheduler()

app = Flask(__name__)
app.config['SECRET_KEY'] = '78587fgrtyth'
login_manager = LoginManager(app)
app.config['UPLOAD_FOLDER'] = 'static/subidas'

# Registrar todas las rutas...
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
register_func_subir_fichero_ts(app)
register_ftp_transfer_routes(app)
register_func_subir_fichero_pallex(app)
register_func_subir_fichero_xpo(app)
register_func_subir_fichero_carreras(app)
register_scanner_ftp_routes(app)

@app.route('/')
def index():
    return redirect(url_for('login'))

@login_manager.user_loader
def load_user(user_id):
    return db.session.query(Usuario).filter_by(id=user_id).first()

# ... resto de rutas igual que main.py ...

if __name__ == '__main__':
    db.Base.metadata.create_all(db.engine)
    # SIN SSL para pruebas rápidas (la cámara puede no funcionar en todos los móviles)
    app.run(debug=True, host='0.0.0.0', port=5000)

