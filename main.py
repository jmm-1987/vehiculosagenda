from flask import Flask, render_template, session, request, redirect, url_for, send_file
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
import db
from ftp_transfer.ftp_transfer import register_ftp_transfer_routes, iniciar_scheduler
from models import Itv, Seguro, Tacografo, Rodaje, Extintor, Usuario, Vehiculo, Taller, IncidenciaAldipod
from datetime import datetime, timedelta
import json
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

# Asegurar columnas nuevas en SQLite al arranque (sin migraciones)
try:
    from db import ensure_column_exists
    ensure_column_exists('incidencia_aldipod', 'tipo_documento', 'VARCHAR(100)', 'INCIDENCIA')
    ensure_column_exists('incidencia_aldipod', 'comunicada', 'BOOLEAN', 0)
    ensure_column_exists('incidencia_aldipod', 'ubicacion', 'VARCHAR(50)', 'Mérida')
except Exception:
    pass

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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        usuario = db.session.query(Usuario).filter_by(username=username).first()
        if usuario and usuario.password == password:
            login_user(usuario)
            return redirect(url_for('portada'))
        else:
            return render_template('login.html', mensaje="Usuario o contraseña incorrectos")
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/portada')
@login_required
def portada():
    """Muestra la pantalla de portada con opciones principales"""
    # Redirección por usuario
    username = session.get('_user_id') and db.session.query(Usuario).filter_by(id=session.get('_user_id')).first()
    if username and username.username == 'email':
        return redirect(url_for('email_destinatarios'))
    
    # Redirección por rol
    try:
        with open('static/roles_config.json', 'r') as f:
            roles = json.load(f)
        username_str = username.username if username else None
        rol = roles.get('roles', {}).get(username_str)
        if rol in ['rep', 'almacen']:
            return redirect(url_for('scanner_clientes'))
        if rol == 'oficina':
            return redirect(url_for('scanner_clientes'))
        if rol == 'incidencias':
            return redirect(url_for('registro_incidencias_aldipod'))
    except Exception:
        pass
    return render_template('portada.html')

@app.route('/index')
@login_required
def home():
    # Redirección por rol
    try:
        with open('static/roles_config.json', 'r') as f:
            roles = json.load(f)
        username = request.args.get('user') or (session.get('_user_id') and db.session.query(Usuario).filter_by(id=session.get('_user_id')).first().username)
        rol = roles.get('roles', {}).get(username)
        if rol in ['rep', 'almacen']:
            return redirect(url_for('scanner_clientes'))
        if rol == 'oficina':
            return redirect(url_for('scanner_clientes'))
        if rol == 'incidencias':
            return redirect(url_for('registro_incidencias_aldipod'))
    except Exception:
        pass
    avisos = []
    ahora = datetime.now().date()
    todas_itv = db.session.query(Itv).all()
    todos_seguros = db.session.query(Seguro).all()
    todos_tacografos = db.session.query(Tacografo).all()
    todos_rodajes = db.session.query(Rodaje).all()
    todos_extintores = db.session.query(Extintor).all()

    # Obtener todos los vehículos
    todos_vehiculos = db.session.query(Vehiculo).filter(Vehiculo.activo == True).all()

    # Contar visitas al taller por matrícula en el último año
    hace_un_ano = ahora - timedelta(days=365)
    tipos_filtrar = ['coche', 'camion', 'remolque']
    vehiculos_filtrados = [v for v in todos_vehiculos if v.tipo and v.tipo.strip().lower() in tipos_filtrar]
    talleres_count_ultimo_ano = {}
    talleres_importe_ultimo_ano = {}
    for v in vehiculos_filtrados:
        count = db.session.query(Taller).filter(Taller.matricula == v.matricula, Taller.fecha_visita >= hace_un_ano).count()
        suma_importe = db.session.query(func.coalesce(func.sum(Taller.importe), 0)).filter(Taller.matricula == v.matricula, Taller.fecha_visita >= hace_un_ano).scalar()
        talleres_count_ultimo_ano[v.matricula] = count
        talleres_importe_ultimo_ano[v.matricula] = suma_importe
    vehiculos_ordenados_taller = sorted(vehiculos_filtrados, key=lambda v: talleres_count_ultimo_ano[v.matricula], reverse=True)

    # Filtrar vehículos por tipo
    vehiculos_seguros = [v for v in todos_vehiculos if v.tipo == 'seguro']
    vehiculos_flota = [v for v in todos_vehiculos if v.tipo in ['camion', 'remolque', 'coche']]

    # Obtener fecha de vencimiento del seguro activo para cada vehículo de seguros y calcular color
    seguros_vencimientos = {}
    seguros_colores = {}
    hoy_dt = ahora
    vehiculos_seguros_fechas = []
    for v in vehiculos_seguros:
        seguro = db.session.query(Seguro).filter_by(matricula=v.matricula, activo=True).order_by(Seguro.venc_seguro.desc()).first()
        if seguro:
            fecha_venc = seguro.venc_seguro
            seguros_vencimientos[v.matricula] = fecha_venc.strftime('%d-%m-%Y')
            dias_restantes = (fecha_venc.date() - hoy_dt).days
            if dias_restantes < 15:
                seguros_colores[v.matricula] = 'red'
            else:
                seguros_colores[v.matricula] = 'black'
            vehiculos_seguros_fechas.append((v, fecha_venc))
        else:
            seguros_vencimientos[v.matricula] = 'Sin seguro activo'
            seguros_colores[v.matricula] = 'black'
            vehiculos_seguros_fechas.append((v, datetime.max))
    # Ordenar por fecha de vencimiento
    vehiculos_seguros = [v for v, _ in sorted(vehiculos_seguros_fechas, key=lambda x: x[1])]

    # --- FLUJO PARA FILTRAR Y MOSTRAR SOLO LOS DE FLOTAS CON VENCIMIENTOS PRÓXIMOS ---
    referencia = hoy_dt + timedelta(days=30)
    flota_vencimientos = {}
    vehiculos_flota_filtrados = []
    for v in vehiculos_flota:
        vencimientos = []
        # ITV
        itv = db.session.query(Itv).filter_by(matricula=v.matricula, activo=True).order_by(Itv.venc_itv.desc()).first()
        if itv and itv.venc_itv.date() < referencia:
            vencimientos.append((itv.venc_itv.date(), f"ITV: {itv.venc_itv.strftime('%d-%m-%Y')}", 'ITV'))
        # Seguro
        seguro = db.session.query(Seguro).filter_by(matricula=v.matricula, activo=True).order_by(Seguro.venc_seguro.desc()).first()
        if seguro and seguro.venc_seguro.date() < referencia:
            vencimientos.append((seguro.venc_seguro.date(), f"Seguro: {seguro.venc_seguro.strftime('%d-%m-%Y')}", 'Seguro'))
        # Tacógrafo
        tacografo = db.session.query(Tacografo).filter_by(matricula=v.matricula, activo=True).order_by(Tacografo.venc_tacografo.desc()).first()
        if tacografo and tacografo.venc_tacografo.date() < referencia:
            vencimientos.append((tacografo.venc_tacografo.date(), f"Tacógrafo: {tacografo.venc_tacografo.strftime('%d-%m-%Y')}", 'Tacógrafo'))
        # Rodaje
        rodaje = db.session.query(Rodaje).filter_by(matricula=v.matricula, activo=True).order_by(Rodaje.venc_rodaje.desc()).first()
        if rodaje and rodaje.venc_rodaje.date() < referencia:
            vencimientos.append((rodaje.venc_rodaje.date(), f"Rodaje: {rodaje.venc_rodaje.strftime('%d-%m-%Y')}", 'Rodaje'))
        # Extintor
        extintor = db.session.query(Extintor).filter_by(matricula=v.matricula, activo=True).order_by(Extintor.venc_ext.desc()).first()
        if extintor and extintor.venc_ext.date() < referencia:
            vencimientos.append((extintor.venc_ext.date(), f"Extintor: {extintor.venc_ext.strftime('%d-%m-%Y')}", 'Extintor'))
        if vencimientos:
            # Tomar el vencimiento más próximo
            vencimiento_proximo = min(vencimientos, key=lambda x: x[0])
            flota_vencimientos[v.matricula] = vencimiento_proximo[1]
            vehiculos_flota_filtrados.append((v, vencimiento_proximo[0]))
    # Ordenar por fecha de vencimiento más próxima
    vehiculos_flota = [v for v, _ in sorted(vehiculos_flota_filtrados, key=lambda x: x[1])]

    for v in todas_itv:
        temporal = v.venc_itv
        if temporal.date() < ahora:
            avisos_itv = []
            avisos_itv.append(temporal.date().strftime("%d-%m-%Y"))
            avisos_itv.append(v.matricula)
            avisos_itv.append("caduca la ITV")
            avisos.append(avisos_itv)
    for v in todos_seguros:
        temporal = v.venc_seguro
        if temporal.date() < ahora:
            avisos_seguros = []
            avisos_seguros.append(temporal.date().strftime("%d-%m-%Y"))
            avisos_seguros.append(v.matricula)
            avisos_seguros.append("vence el seguro")
            avisos.append(avisos_seguros)
    for v in todos_tacografos:
        temporal = v.venc_tacografo
        if temporal.date() < ahora:
            avisos_tacografos = []
            avisos_tacografos.append(temporal.date().strftime("%d-%m-%Y"))
            avisos_tacografos.append(v.matricula)
            avisos_tacografos.append("caduca el tacógrafo")
            avisos.append(avisos_tacografos)
    for v in todos_rodajes:
        temporal = v.venc_rodaje
        if temporal.date() < ahora:
            avisos_rodajes = []
            avisos_rodajes.append(temporal.date().strftime("%d-%m-%Y"))
            avisos_rodajes.append(v.matricula)
            avisos_rodajes.append("renovacion del rodaje")
            avisos.append(avisos_rodajes)
    for v in todos_extintores:
        temporal = v.venc_ext
        if temporal.date() < ahora:
            avisos_extintores = []  
            avisos_extintores.append(temporal.date().strftime("%d-%m-%Y"))
            avisos_extintores.append(v.matricula)
            avisos_extintores.append("caducidad extintores")
            avisos.append(avisos_extintores)

    avisos = sorted(avisos, key=lambda x: x[0])

    return render_template('index.html', avisos=avisos, vehiculos_seguros=vehiculos_seguros, vehiculos_flota=vehiculos_flota, hoy=ahora.strftime('%Y-%m-%d'), seguros_vencimientos=seguros_vencimientos, seguros_colores=seguros_colores, flota_vencimientos=flota_vencimientos, talleres_count_ultimo_ano=talleres_count_ultimo_ano, talleres_importe_ultimo_ano=talleres_importe_ultimo_ano, vehiculos_ordenados_taller=vehiculos_ordenados_taller)

@app.route('/email_destinatarios', methods=['GET', 'POST'])
@login_required
def email_destinatarios():
    from urllib.parse import quote
    from urllib.parse import urlencode
    
    if request.method == 'POST':
        agencia = request.form.get('agencia')
        proveedor = request.form.get('proveedor')
        email_destinatario = request.form.get('email_destinatario')
        
        if agencia == 'tsb':
            tracking = request.form.get('tsb_tracking')
            if tracking:
                url_tracking = f"https://www.tsbconnect.net/tracking/search?number={tracking}"
                email_text = f"Hola,\n\nEn los próximos días recibirá un pedido de su proveedor {proveedor} a través de la agencia TSB.\n\nPuede hacer seguimiento aquí: {url_tracking}"
                subject = "Seguimiento de Pedido TSB"
                body = quote(email_text)
                mailto_link = f"mailto:{email_destinatario}?subject={quote(subject)}&body={body}"
                return render_template('email_destinatarios.html', email_text=email_text, mailto_link=mailto_link, url_tracking=url_tracking)
        elif agencia == 'pallex':
            tracking = request.form.get('pallex_tracking')
            postal = request.form.get('pallex_postal')
            if tracking and postal:
                url_tracking = f"https://mynexus.pallex.com/tracking"
                email_text = f"Hola,\n\nEn los próximos días recibirá un pedido de su proveedor {proveedor} a través de la agencia PALLEX.\n\nPuede hacer seguimiento aquí: {url_tracking}\nNúmero tracking: {tracking}\nCódigo postal destino: {postal}"
                subject = "Seguimiento de Pedido PALLEX"
                body = quote(email_text)
                mailto_link = f"mailto:{email_destinatario}?subject={quote(subject)}&body={body}"
                return render_template('email_destinatarios.html', email_text=email_text, mailto_link=mailto_link, url_tracking=url_tracking)
    
    return render_template('email_destinatarios.html')

@app.route('/descargar_db')
@login_required
def descargar_db():
    fecha = datetime.now().strftime('%d%m%Y')
    nombre = f'VEHICULOS_{fecha}.db'
    return send_file(
        'database/VEHICULOS.db',
        as_attachment=True,
        download_name=nombre
    )


if __name__ == '__main__':
    db.Base.metadata.create_all(db.engine)
    # Usar SSL para permitir acceso a la cámara desde móviles
    # Opción 1: Con certificados generados (descomentar si los certificados existen)
    # app.run(debug=True, host='0.0.0.0', port=5000, ssl_context=('cert.pem', 'key.pem'))
    
    # Opción 2: SSL adhoc (más simple, genera certificados temporales automáticamente)
    app.run(debug=True, host='0.0.0.0', port=5000, ssl_context='adhoc')


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
