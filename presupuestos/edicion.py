from flask import render_template, request, redirect, url_for
from flask_login import login_required
import db
from datetime import datetime
from models import Presupuesto, ClientePresupuesto


def register_presupuestoedit_routes(app):
    @app.route('/form_editar_presupuesto/<id>')
    @login_required
    def edicion_presupuesto(id):
        presupuesto_editar = db.session.query(Presupuesto).filter_by(id=id).first()
        if not presupuesto_editar:
            return redirect(url_for('lista_presupuestos'))
        
        # Obtener todos los clientes activos para el dropdown
        clientes = db.session.query(ClientePresupuesto).filter(
            ClientePresupuesto.activo == True
        ).order_by(ClientePresupuesto.nombre).all()
        
        # Calcular IVA percent desde iva e importe
        iva_percent = 0
        if presupuesto_editar.importe and presupuesto_editar.importe > 0:
            iva_percent = (presupuesto_editar.iva / presupuesto_editar.importe) * 100
        
        return render_template("form_editar_presupuesto.html", 
                             presupuesto_editar=presupuesto_editar,
                             lista_clientes=clientes,
                             iva_percent=iva_percent)

    @app.route("/modificar_presupuesto", methods=['POST'])
    @login_required
    def modificar_presupuesto():
        id = request.form["id"]
        presupuesto_modificar = db.session.query(Presupuesto).filter_by(id=id).first()
        
        if not presupuesto_modificar:
            return redirect(url_for('lista_presupuestos'))
        
        # Actualizar campos
        fecha_presupuesto_str = request.form.get("fecha_presupuesto")
        if fecha_presupuesto_str:
            presupuesto_modificar.fecha_presupuesto = datetime.strptime(fecha_presupuesto_str, '%Y-%m-%d')
        
        cliente_id_str = request.form.get("cliente_id", "0")
        try:
            cliente_id = int(cliente_id_str)
            if cliente_id:
                presupuesto_modificar.cliente_id = cliente_id
        except (ValueError, TypeError):
            pass
        
        presupuesto_modificar.concepto = request.form.get("concepto", "")
        
        try:
            importe = float(request.form.get("importe", 0) or 0)
            presupuesto_modificar.importe = importe
        except (ValueError, TypeError):
            pass
        
        try:
            iva = float(request.form.get("iva", 0) or 0)
            presupuesto_modificar.iva = iva
        except (ValueError, TypeError):
            pass
        
        try:
            total = float(request.form.get("total", 0) or 0)
            presupuesto_modificar.total = total
        except (ValueError, TypeError):
            pass
        
        presupuesto_modificar.estado = request.form.get("estado", "PENDIENTE")
        presupuesto_modificar.observaciones = request.form.get("observaciones", "")
        
        db.session.commit()
        return redirect(url_for('lista_presupuestos'))

