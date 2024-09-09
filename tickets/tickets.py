from flask import render_template, redirect, url_for, request
from flask_login import login_required
import db
from datetime import datetime, timedelta, date
from models import Ticket, Vehiculo
from sqlalchemy import func, desc

def register_tickets_routes(app):
    @app.route('/selector', methods=['GET', 'POST'])
    @login_required
    def selector():
        todos_los_vehiculos = db.session.query(Vehiculo).filter(Vehiculo.tipo=="camion").all()
        return render_template('selector.html', lista_vehiculos=todos_los_vehiculos)

    @app.route('/gasoil', methods=['GET', 'POST'])
    def lista_tickets():
        matriculas = db.session.query(Vehiculo.matricula).all()
        todos_tickets = db.session.query(Ticket).all()
        return render_template('gasoil.html', lista_tickets=todos_tickets, lista_matriculas=matriculas)

    @app.route('/formulario_gasoil')
    def formulario_gasoil():
        matriculas = db.session.query(Vehiculo.matricula).filter(Vehiculo.tipo == "camion").all()
        return render_template("crear_ticket.html", lista_matriculas=matriculas)

    @app.route("/borrar_ticket/<id>", methods=["POST", "GET"])
    def borrar_ticket(id):
        registro_borrar = db.session.query(Ticket).filter_by(id=id).first()
        db.session.delete(registro_borrar)
        db.session.commit()
        registro_para_url = db.session.query(Vehiculo.id).filter_by(matricula=registro_borrar.matricula).scalar()
        return redirect(url_for('buscador_tickets_selector', id=registro_para_url))

    @app.route("/crear_ticket", methods=["POST", "GET"])
    def crear_ticket():
        fecha_ticket_str = request.form["fecha_ticket"]
        fecha_ticket = datetime.strptime(fecha_ticket_str, '%Y-%m-%d')
        ticket = Ticket(matricula=request.form["matricula"],
                        fecha_ticket=datetime.strptime(request.form["fecha_ticket"], '%Y-%m-%d'),
                        tipo_ticket = request.form["tipo"],
                        kms_ticket=request.form["kms_ticket"],
                        litros_ticket=request.form["litros_ticket"],
                        precio_ticket=request.form["precio_ticket"],
                        precio_litro_ticket=round(
                            float(request.form["precio_ticket"]) / float(request.form["litros_ticket"]), 2),
                        obs_ticket=request.form["obs_ticket"])
        db.session.add(ticket)
        db.session.commit()
        return redirect(url_for('selector'))

    @app.route('/gasoil_busqueda_selector/<id>', methods=["GET", 'POST'])
    def buscador_tickets_selector(id):
        veh_select_mat = db.session.query(Vehiculo.matricula).filter_by(id=(id)).scalar()
        if request.method == 'POST':
            veh_select_mat = request.form["mat"]
            fecha_inicio = datetime.strptime(request.form["fecha_inicio"], '%Y-%m-%d').date()
            fecha_fin = datetime.strptime(request.form["fecha_fin"], '%Y-%m-%d').date()
        else:
            fecha_actual = date.today()
            fecha_inicio= fecha_actual - timedelta(days=31)
            fecha_fin = datetime.now().date()

        tickets_busqueda = db.session.query(Ticket).filter(
            Ticket.matricula == veh_select_mat,
            Ticket.fecha_ticket >= fecha_inicio,
            Ticket.fecha_ticket <= fecha_fin
        ).order_by(Ticket.fecha_ticket).all()

        total_gasoil = db.session.query(func.sum(Ticket.litros_ticket)).filter(
            Ticket.matricula == veh_select_mat,
            Ticket.fecha_ticket >= fecha_inicio,
            Ticket.fecha_ticket <= fecha_fin,
            Ticket.tipo_ticket == 'gasoil'
        ).scalar()
        if total_gasoil == None:
            total_gasoil = 0

        total_euros_gasoil = db.session.query(func.sum(Ticket.precio_ticket)).filter(
            Ticket.matricula == veh_select_mat,
            Ticket.fecha_ticket >= fecha_inicio,
            Ticket.fecha_ticket <= fecha_fin,
            Ticket.tipo_ticket == 'gasoil'
        ).scalar()

        total_euros_addblue = db.session.query(func.sum(Ticket.precio_ticket)).filter(
            Ticket.matricula == veh_select_mat,
            Ticket.fecha_ticket >= fecha_inicio,
            Ticket.fecha_ticket <= fecha_fin,
            Ticket.tipo_ticket == 'addblue'
        ).scalar()
        if total_euros_addblue == None:
            total_euros_addblue = 0

        total_addblue = db.session.query(func.sum(Ticket.litros_ticket)).filter(
            Ticket.matricula == veh_select_mat,
            Ticket.fecha_ticket >= fecha_inicio,
            Ticket.fecha_ticket <= fecha_fin,
            Ticket.tipo_ticket == 'addblue'
        ).scalar()
        if total_addblue == None:
            total_addblue = 0

        media_gasoil = db.session.query(func.avg(Ticket.precio_litro_ticket)).filter(
            Ticket.matricula == veh_select_mat,
            Ticket.fecha_ticket >= fecha_inicio,
            Ticket.fecha_ticket <= fecha_fin,
            Ticket.tipo_ticket == 'gasoil'
        ).scalar()

        media_addblue = db.session.query(func.avg(Ticket.precio_litro_ticket)).filter(
            Ticket.matricula == veh_select_mat,
            Ticket.fecha_ticket >= fecha_inicio,
            Ticket.fecha_ticket <= fecha_fin,
            Ticket.tipo_ticket == 'addblue'
        ).scalar()
        if media_addblue == None:
            media_addblue = 0

        primer_ticket = db.session.query(Ticket).filter(
            Ticket.matricula == veh_select_mat,
            Ticket.fecha_ticket >= fecha_inicio,
            Ticket.fecha_ticket <= fecha_fin,
        ).order_by(Ticket.fecha_ticket).first()

        ultimo_ticket = db.session.query(Ticket).filter(
            Ticket.matricula == veh_select_mat,
            Ticket.fecha_ticket >= fecha_inicio,
            Ticket.fecha_ticket <= fecha_fin,
        ).order_by(desc(Ticket.fecha_ticket)).first()

        # Calcular la diferencia de kilómetros si se encuentran tanto el primer como el último ticket
        if primer_ticket and ultimo_ticket:
            km_inicial = primer_ticket.kms_ticket
            km_final = ultimo_ticket.kms_ticket
            km_recorridos = km_final - km_inicial
        else:
            km_recorridos = 0  # O algún valor predeterminado si no hay suficientes datos

        if total_euros_gasoil != 0 and km_recorridos != 0:
            total_menos_ultimo = total_euros_gasoil - ultimo_ticket.precio_ticket
            precio_km = total_menos_ultimo / km_recorridos
        else:
            precio_km = 0

        total_gasoil = total_gasoil if total_gasoil is not None else 0
        total_addblue = total_addblue if total_addblue is not None else 0
        total_euros_gasoil = total_euros_gasoil if total_euros_gasoil is not None else 0
        total_euros_addblue = total_euros_addblue if total_euros_addblue is not None else 0
        media_gasoil = media_gasoil if media_gasoil is not None else 0
        media_addblue = media_addblue if media_addblue is not None else 0
        km_recorridos = km_recorridos if km_recorridos is not None else 0
        precio_km = precio_km if precio_km is not None else 0

        return render_template('gasoil_busqueda_selector.html', lista_tickets=tickets_busqueda,
                                                                                  veh_select_mat=veh_select_mat,
                                                                                  fecha_inicio=fecha_inicio,
                                                                                  fecha_fin=fecha_fin,
                                                                                  total_gasoil=total_gasoil,
                                                                                  total_addblue=total_addblue,
                                                                                  total_euros_gasoil=total_euros_gasoil,
                                                                                  total_euros_addblue=total_euros_addblue,
                                                                                  media_gasoil=media_gasoil,
                                                                                  media_addblue=media_addblue,
                                                                                  km_recorridos=km_recorridos,
                                                                                  precio_km=precio_km)


