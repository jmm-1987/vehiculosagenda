from flask import render_template, redirect, url_for, request, jsonify, send_file
from flask_login import login_required, current_user
import db
from datetime import datetime
from models import Presupuesto, ClientePresupuesto
from sqlalchemy import func
from presupuestos.generar_pdf import generar_pdf_presupuesto
import os


def register_presupuestos_routes(app):
    @app.route('/presupuestos')
    @login_required
    def lista_presupuestos():
        todos_presupuestos = db.session.query(Presupuesto, ClientePresupuesto).join(
            ClientePresupuesto, Presupuesto.cliente_id == ClientePresupuesto.id
        ).filter(Presupuesto.activo == True).order_by(Presupuesto.fecha_presupuesto.desc()).all()
        clientes = db.session.query(ClientePresupuesto).filter(ClientePresupuesto.activo == True).order_by(ClientePresupuesto.nombre).all()
        return render_template('presupuestos.html', lista_presupuestos=todos_presupuestos, lista_clientes=clientes)

    @app.route('/presupuestos_todos')
    @login_required
    def lista_presupuestos_todos():
        todos_presupuestos = db.session.query(Presupuesto, ClientePresupuesto).join(
            ClientePresupuesto, Presupuesto.cliente_id == ClientePresupuesto.id
        ).order_by(Presupuesto.fecha_presupuesto.desc()).all()
        clientes = db.session.query(ClientePresupuesto).filter(ClientePresupuesto.activo == True).order_by(ClientePresupuesto.nombre).all()
        return render_template('presupuestos.html', lista_presupuestos=todos_presupuestos, lista_clientes=clientes)

    @app.route('/formulario_presupuesto')
    @login_required
    def formulario_presupuesto():
        clientes = db.session.query(ClientePresupuesto).filter(ClientePresupuesto.activo == True).order_by(ClientePresupuesto.nombre).all()
        return render_template("crear_presupuesto.html", lista_clientes=clientes)
    
    @app.route('/siguiente_numero_presupuesto')
    @login_required
    def siguiente_numero_presupuesto():
        """Obtiene el siguiente número de presupuesto disponible"""
        try:
            # Obtener el último ID para asegurar secuencia
            ultimo_id = db.session.query(func.max(Presupuesto.id)).scalar()
            siguiente_num = (ultimo_id or 0) + 1
            return jsonify({"numero": siguiente_num})
        except Exception as e:
            return jsonify({"numero": 1})
    
    @app.route('/crear_cliente_presupuesto', methods=['POST'])
    @login_required
    def crear_cliente_presupuesto():
        try:
            nombre = request.form.get("nombre", "").strip()
            cif = request.form.get("cif", "").strip()
            direccion = request.form.get("direccion", "").strip()
            poblacion = request.form.get("poblacion", "").strip()
            telefono = request.form.get("telefono", "").strip()
            email = request.form.get("email", "").strip()
            
            if not nombre or not cif or not direccion:
                return jsonify({"success": False, "error": "Los campos Nombre, CIF y Dirección son obligatorios"}), 400
            
            # Verificar si ya existe un cliente con el mismo CIF
            cliente_existente = db.session.query(ClientePresupuesto).filter_by(cif=cif, activo=True).first()
            if cliente_existente:
                return jsonify({"success": False, "error": "Ya existe un cliente con este CIF"}), 400
            
            cliente = ClientePresupuesto(
                nombre=nombre,
                cif=cif,
                direccion=direccion,
                poblacion=poblacion,
                telefono=telefono,
                email=email
            )
            
            db.session.add(cliente)
            db.session.commit()
            
            return jsonify({
                "success": True, 
                "cliente": {
                    "id": cliente.id,
                    "nombre": cliente.nombre,
                    "cif": cliente.cif
                }
            })
        except Exception as e:
            db.session.rollback()
            return jsonify({"success": False, "error": str(e)}), 500

    @app.route("/borrar_presupuesto/<id>", methods=["POST", "GET"])
    @login_required
    def borrar_presupuesto(id):
        registro_borrar = db.session.query(Presupuesto).filter_by(id=id).first()
        if registro_borrar:
            registro_borrar.activo = False
            db.session.commit()
        return redirect(url_for('lista_presupuestos'))

    @app.route("/crear_presupuesto", methods=["POST"])
    @login_required
    def crear_presupuesto():
        try:
            # Generar número de presupuesto automáticamente
            numero_presupuesto_input = request.form.get("numero_presupuesto", "").strip()
            if numero_presupuesto_input:
                numero_presupuesto = numero_presupuesto_input
            else:
                # Obtener el último ID y sumar 1
                ultimo_id = db.session.query(func.max(Presupuesto.id)).scalar() or 0
                numero_presupuesto = str(ultimo_id + 1)
            
            fecha_presupuesto_str = request.form.get("fecha_presupuesto")
            cliente_id_str = request.form.get("cliente_id", "0")
            try:
                cliente_id = int(cliente_id_str)
            except (ValueError, TypeError):
                cliente_id = 0
            
            if not cliente_id:
                return jsonify({"success": False, "error": "Debe seleccionar un cliente"}), 400
            
            concepto = request.form.get("concepto", "")  # Mantener por compatibilidad
            bultos = request.form.get("bultos", "")
            kg = request.form.get("kg", "")
            medidas = request.form.get("medidas", "")
            
            # Validar campos obligatorios
            if not bultos or not kg or not medidas:
                return jsonify({"success": False, "error": "Los campos Bultos, Kg y Medidas son obligatorios"}), 400
            
            try:
                importe = float(request.form.get("importe", 0) or 0)
            except (ValueError, TypeError):
                importe = 0.0
            try:
                iva = float(request.form.get("iva", 0) or 0)
            except (ValueError, TypeError):
                iva = 0.0
            try:
                total = float(request.form.get("total", 0) or 0)
            except (ValueError, TypeError):
                total = 0.0
            estado = request.form.get("estado", "PENDIENTE")
            observaciones = request.form.get("observaciones", "")
            
            fecha_presupuesto = datetime.strptime(fecha_presupuesto_str, '%Y-%m-%d') if fecha_presupuesto_str else datetime.now()
            fecha_creacion = datetime.now()
            
            presupuesto = Presupuesto(
                numero_presupuesto=numero_presupuesto,
                fecha_presupuesto=fecha_presupuesto,
                cliente_id=cliente_id,
                concepto=concepto,  # Mantener por compatibilidad
                bultos=bultos,
                kg=kg,
                medidas=medidas,
                importe=importe,
                iva=iva,
                total=total,
                estado=estado,
                observaciones=observaciones,
                fecha_creacion=fecha_creacion,
                usuario_creacion=current_user.username if current_user else ""
            )
            
            db.session.add(presupuesto)
            db.session.commit()
            return redirect(url_for('lista_presupuestos'))
        except Exception as e:
            db.session.rollback()
            import traceback
            error_traceback = traceback.format_exc()
            print(f"Error al crear presupuesto: {str(e)}")
            print(f"Traceback: {error_traceback}")
            # Siempre devolver JSON para peticiones desde el modal
            return jsonify({"success": False, "error": str(e), "traceback": error_traceback}), 400

    @app.route("/exportar_presupuesto_pdf/<id>")
    @login_required
    def exportar_presupuesto_pdf(id):
        """Exporta un presupuesto a PDF"""
        try:
            from io import BytesIO
            
            presupuesto = db.session.query(Presupuesto).filter_by(id=id).first()
            if not presupuesto:
                return jsonify({"error": "Presupuesto no encontrado"}), 404
            
            cliente = db.session.query(ClientePresupuesto).filter_by(id=presupuesto.cliente_id).first()
            if not cliente:
                return jsonify({"error": "Cliente no encontrado"}), 404
            
            # Generar PDF en memoria cada vez (sin guardar en servidor)
            # Siempre generar de nuevo para tener los datos más actualizados
            pdf_bytes = generar_pdf_presupuesto(presupuesto, cliente, output_path=None)
            
            # Crear objeto BytesIO para enviar el PDF
            pdf_io = BytesIO(pdf_bytes)
            pdf_io.seek(0)
            
            # Agregar timestamp al nombre para evitar cache del navegador
            from datetime import datetime
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            # Enviar archivo directamente desde memoria con headers para evitar cache
            response = send_file(
                pdf_io,
                as_attachment=True,
                download_name=f'presupuesto_{presupuesto.numero_presupuesto}_{timestamp}.pdf',
                mimetype='application/pdf'
            )
            
            # Headers para evitar cache del navegador
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
            
            return response
        except Exception as e:
            import traceback
            error_traceback = traceback.format_exc()
            print(f"Error al generar PDF: {str(e)}")
            print(f"Traceback: {error_traceback}")
            return jsonify({"error": str(e)}), 500

