from flask import render_template, redirect, url_for, request, jsonify, send_file, flash
from flask_login import login_required, current_user
import db
from datetime import datetime
from models import Presupuesto, ClientePresupuesto, FacturaProforma
from sqlalchemy import func
from presupuestos.generar_pdf import generar_pdf_presupuesto
from presupuestos.generar_pdf_factura_proforma import generar_pdf_factura_proforma
import os


def register_presupuestos_routes(app):
    @app.route('/presupuestos')
    @login_required
    def lista_presupuestos():
        todos_presupuestos = db.session.query(Presupuesto, ClientePresupuesto).join(
            ClientePresupuesto, Presupuesto.cliente_id == ClientePresupuesto.id
        ).filter(Presupuesto.activo == True).order_by(Presupuesto.id.desc()).all()
        clientes = db.session.query(ClientePresupuesto).filter(ClientePresupuesto.activo == True).order_by(ClientePresupuesto.nombre).all()
        return render_template('presupuestos.html', lista_presupuestos=todos_presupuestos, lista_clientes=clientes)

    @app.route('/presupuestos_todos')
    @login_required
    def lista_presupuestos_todos():
        todos_presupuestos = db.session.query(Presupuesto, ClientePresupuesto).join(
            ClientePresupuesto, Presupuesto.cliente_id == ClientePresupuesto.id
        ).order_by(Presupuesto.id.desc()).all()
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

    @app.route('/presupuestos/clientes')
    @login_required
    def lista_clientes_presupuestos():
        """Lista todos los clientes de presupuestos"""
        clientes = db.session.query(ClientePresupuesto).order_by(ClientePresupuesto.nombre).all()
        return render_template('clientes_presupuestos.html', lista_clientes=clientes)

    @app.route('/presupuestos/clientes/editar/<int:id>', methods=['GET', 'POST'])
    @login_required
    def editar_cliente_presupuesto(id):
        """Editar un cliente de presupuestos"""
        cliente = db.session.query(ClientePresupuesto).filter_by(id=id).first()
        if not cliente:
            flash('Cliente no encontrado', 'error')
            return redirect(url_for('lista_clientes_presupuestos'))
        
        if request.method == 'POST':
            try:
                nombre = request.form.get("nombre", "").strip()
                cif = request.form.get("cif", "").strip()
                direccion = request.form.get("direccion", "").strip()
                poblacion = request.form.get("poblacion", "").strip()
                telefono = request.form.get("telefono", "").strip()
                email = request.form.get("email", "").strip()
                activo = request.form.get("activo") == "on"
                
                if not nombre or not cif or not direccion:
                    flash('Los campos Nombre, CIF y Dirección son obligatorios', 'error')
                    return redirect(url_for('editar_cliente_presupuesto', id=id))
                
                # Verificar si ya existe otro cliente con el mismo CIF (excluyendo el actual)
                cliente_existente = db.session.query(ClientePresupuesto).filter(
                    ClientePresupuesto.cif == cif,
                    ClientePresupuesto.id != id,
                    ClientePresupuesto.activo == True
                ).first()
                if cliente_existente:
                    flash('Ya existe otro cliente activo con este CIF', 'error')
                    return redirect(url_for('editar_cliente_presupuesto', id=id))
                
                cliente.nombre = nombre
                cliente.cif = cif
                cliente.direccion = direccion
                cliente.poblacion = poblacion
                cliente.telefono = telefono
                cliente.email = email
                cliente.activo = activo
                
                db.session.commit()
                flash('Cliente actualizado correctamente', 'success')
                return redirect(url_for('lista_clientes_presupuestos'))
            except Exception as e:
                db.session.rollback()
                flash(f'Error al actualizar cliente: {str(e)}', 'error')
        
        return render_template('form_editar_cliente_presupuesto.html', cliente=cliente)

    @app.route("/generar_factura_proforma/<int:id>", methods=['POST', 'GET'])
    @login_required
    def generar_factura_proforma(id):
        """Genera una factura proforma desde un presupuesto aprobado"""
        try:
            presupuesto = db.session.query(Presupuesto).filter_by(id=id).first()
            if not presupuesto:
                flash('Presupuesto no encontrado', 'error')
                return redirect(url_for('lista_presupuestos'))
            
            if presupuesto.estado != 'APROBADO':
                flash('Solo se pueden generar facturas proforma de presupuestos aprobados', 'error')
                return redirect(url_for('lista_presupuestos'))
            
            # Verificar si ya existe una factura proforma para este presupuesto
            factura_existente = db.session.query(FacturaProforma).filter_by(presupuesto_id=id).first()
            if factura_existente:
                flash('Ya existe una factura proforma para este presupuesto', 'info')
                return redirect(url_for('exportar_factura_proforma_pdf', id=factura_existente.id))
            
            cliente = db.session.query(ClientePresupuesto).filter_by(id=presupuesto.cliente_id).first()
            if not cliente:
                flash('Cliente no encontrado', 'error')
                return redirect(url_for('lista_presupuestos'))
            
            # Generar número de factura proforma: año + contador
            año_actual = datetime.now().year
            # Obtener el último número de factura proforma del año actual
            ultima_factura = db.session.query(FacturaProforma).filter(
                FacturaProforma.numero_factura_proforma.like(f"{año_actual}%")
            ).order_by(FacturaProforma.id.desc()).first()
            
            if ultima_factura:
                # Extraer el número del último formato (año + número)
                try:
                    ultimo_numero = int(ultima_factura.numero_factura_proforma.replace(str(año_actual), ''))
                    siguiente_numero = ultimo_numero + 1
                except:
                    siguiente_numero = 1
            else:
                siguiente_numero = 1
            
            numero_factura_proforma = f"{año_actual}{siguiente_numero:04d}"  # Formato: 20260001
            
            # Crear factura proforma
            factura_proforma = FacturaProforma(
                numero_factura_proforma=numero_factura_proforma,
                fecha_factura_proforma=datetime.now(),
                presupuesto_id=presupuesto.id,
                cliente_id=presupuesto.cliente_id,
                bultos=presupuesto.bultos,
                kg=presupuesto.kg,
                medidas=presupuesto.medidas,
                importe=presupuesto.importe,
                iva=presupuesto.iva,
                total=presupuesto.total,
                observaciones=presupuesto.observaciones,
                fecha_creacion=datetime.now(),
                usuario_creacion=current_user.username if current_user else ""
            )
            
            db.session.add(factura_proforma)
            db.session.commit()
            
            flash(f'Factura proforma {numero_factura_proforma} generada correctamente', 'success')
            return redirect(url_for('exportar_factura_proforma_pdf', id=factura_proforma.id))
            
        except Exception as e:
            db.session.rollback()
            import traceback
            error_traceback = traceback.format_exc()
            print(f"Error al generar factura proforma: {str(e)}")
            print(f"Traceback: {error_traceback}")
            flash(f'Error al generar factura proforma: {str(e)}', 'error')
            return redirect(url_for('lista_presupuestos'))

    @app.route("/exportar_factura_proforma_pdf/<int:id>")
    @login_required
    def exportar_factura_proforma_pdf(id):
        """Exporta una factura proforma a PDF"""
        try:
            from io import BytesIO
            
            factura_proforma = db.session.query(FacturaProforma).filter_by(id=id).first()
            if not factura_proforma:
                return jsonify({"error": "Factura proforma no encontrada"}), 404
            
            presupuesto = db.session.query(Presupuesto).filter_by(id=factura_proforma.presupuesto_id).first()
            if not presupuesto:
                return jsonify({"error": "Presupuesto no encontrado"}), 404
            
            cliente = db.session.query(ClientePresupuesto).filter_by(id=factura_proforma.cliente_id).first()
            if not cliente:
                return jsonify({"error": "Cliente no encontrado"}), 404
            
            # Generar PDF en memoria
            pdf_bytes = generar_pdf_factura_proforma(factura_proforma, presupuesto, cliente, output_path=None)
            
            # Crear objeto BytesIO para enviar el PDF
            pdf_io = BytesIO(pdf_bytes)
            pdf_io.seek(0)
            
            # Agregar timestamp al nombre para evitar cache del navegador
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            # Enviar archivo directamente desde memoria con headers para evitar cache
            response = send_file(
                pdf_io,
                as_attachment=True,
                download_name=f'factura_proforma_{factura_proforma.numero_factura_proforma}_{timestamp}.pdf',
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
            print(f"Error al generar PDF de factura proforma: {str(e)}")
            print(f"Traceback: {error_traceback}")
            return jsonify({"error": str(e)}), 500
