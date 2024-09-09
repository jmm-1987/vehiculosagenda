from flask import redirect, url_for, request
import db
from models import Ticket, Vehiculo

def register_funciones_tickets_routes(app):
    @app.route("/marcar_ticket", methods=["POST","GET"])
    def marcar():
        marcar = request.form["marcar"]
        registro_marcar = db.session.query(Ticket).filter_by(id=marcar).first()
        registro_marcar.marcado = True
        db.session.commit()
        registro_para_url = db.session.query(Vehiculo.id).filter_by(matricula=registro_marcar.matricula).scalar()
        return redirect(url_for("buscador_tickets_selector", id=registro_para_url))

    @app.route("/desmarcar_ticket", methods=["POST","GET"])
    def desmarcar():
        desmarcar = request.form["desmarcar"]
        registro_marcar = db.session.query(Ticket).filter_by(id=desmarcar).first()
        registro_marcar.marcado = False
        db.session.commit()
        registro_para_url = db.session.query(Vehiculo.id).filter_by(matricula=registro_marcar.matricula).scalar()
        return redirect(url_for("buscador_tickets_selector", id=registro_para_url))


    @app.route("/facturar_ticket", methods=["GET"])
    def facturar():
        matricula = request.args.get("mat")
        fecha_inicio = request.args.get("fecha_inicio")
        print(fecha_inicio)
        tickets_facturar = db.session.query(Ticket).filter_by(matricula=matricula, marcado=True).all()
        for f in tickets_facturar:
            f.facturado = True
        db.session.commit()
        registro_para_url = db.session.query(Vehiculo.id).filter_by(matricula=matricula).scalar()
        return redirect(url_for('buscador_tickets_selector', id=registro_para_url))
