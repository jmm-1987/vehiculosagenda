"""
Rutas para el módulo de Caja (Cobros, Pagos y Arqueo)
Soporta dos tipos de caja: CAJA y REEMBOLSOS
"""
from flask import render_template, request, redirect, url_for, jsonify, flash
from flask_login import login_required, current_user
from functools import wraps
from models import CajaCobro, CajaPago, CajaArqueo
from datetime import datetime, date
import db
from sqlalchemy import func
import sys


def register_caja_routes(app):
    """Registra las rutas del módulo de Caja"""
    
    def solo_reembolsos_required(f):
        """Decorador para restringir acceso: usuario 'caja' solo puede acceder a reembolsos"""
        @wraps(f)
        @login_required
        def decorated_function(*args, **kwargs):
            if current_user.username == 'caja':
                flash('No tienes acceso a esta sección. Solo puedes acceder a Caja Reembolsos.', 'error')
                return redirect(url_for('caja_reembolsos_index'))
            return f(*args, **kwargs)
        return decorated_function
    
    # ========== CAJA NORMAL ==========
    @app.route('/caja')
    @solo_reembolsos_required
    def caja_index():
        """Página principal de Caja con Cobros y Pagos en la misma pantalla"""
        return _caja_index('CAJA', 'Caja')
    
    @app.route('/caja/cobros')
    @solo_reembolsos_required
    def caja_cobros():
        """Lista de cobros no arqueados de Caja normal"""
        return _caja_cobros('CAJA')
    
    @app.route('/caja/cobros/crear', methods=['GET', 'POST'])
    @solo_reembolsos_required
    def crear_cobro():
        """Crear nuevo cobro en Caja normal"""
        return _crear_cobro('CAJA', 'caja_cobros')
    
    @app.route('/caja/cobros/editar/<int:id>', methods=['GET', 'POST'])
    @solo_reembolsos_required
    def editar_cobro(id):
        """Editar cobro existente de Caja normal"""
        return _editar_cobro(id, 'CAJA', 'caja_cobros')
    
    @app.route('/caja/cobros/eliminar/<int:id>', methods=['POST'])
    @solo_reembolsos_required
    def eliminar_cobro(id):
        """Eliminar cobro de Caja normal"""
        return _eliminar_cobro(id, 'CAJA', 'caja_cobros')
    
    @app.route('/caja/pagos')
    @solo_reembolsos_required
    def caja_pagos():
        """Lista de pagos no arqueados de Caja normal"""
        return _caja_pagos('CAJA')
    
    @app.route('/caja/pagos/crear', methods=['GET', 'POST'])
    @solo_reembolsos_required
    def crear_pago():
        """Crear nuevo pago en Caja normal"""
        return _crear_pago('CAJA', 'caja_pagos')
    
    @app.route('/caja/pagos/editar/<int:id>', methods=['GET', 'POST'])
    @solo_reembolsos_required
    def editar_pago(id):
        """Editar pago existente de Caja normal"""
        return _editar_pago(id, 'CAJA', 'caja_pagos')
    
    @app.route('/caja/pagos/eliminar/<int:id>', methods=['POST'])
    @solo_reembolsos_required
    def eliminar_pago(id):
        """Eliminar pago de Caja normal"""
        return _eliminar_pago(id, 'CAJA', 'caja_pagos')
    
    @app.route('/caja/arqueo')
    @solo_reembolsos_required
    def caja_arqueo():
        """Página de arqueo de Caja normal"""
        return _caja_arqueo('CAJA', 'Caja')
    
    @app.route('/caja/arqueo/<int:id>', endpoint='ver_arqueo_detalle')
    @solo_reembolsos_required
    def ver_arqueo_detalle(id):
        """Ver detalles de un arqueo de Caja normal"""
        return _ver_arqueo_detalle(id, 'CAJA', 'Caja')
    
    @app.route('/caja/arqueo/procesar', methods=['POST'])
    @solo_reembolsos_required
    def procesar_arqueo():
        """Procesar arqueo de Caja normal"""
        return _procesar_arqueo('CAJA', 'caja_arqueo')
    
    # ========== CAJA REEMBOLSOS ==========
    @app.route('/caja-reembolsos', endpoint='caja_reembolsos_index')
    @login_required
    def caja_reembolsos_index():
        """Página principal de Caja Reembolsos con Cobros y Pagos en la misma pantalla"""
        return _caja_index('REEMBOLSOS', 'Caja Reembolsos')
    
    @app.route('/caja-reembolsos/cobros', endpoint='caja_reembolsos_cobros')
    @login_required
    def caja_reembolsos_cobros():
        """Lista de cobros no arqueados de Caja Reembolsos"""
        return _caja_cobros('REEMBOLSOS')
    
    @app.route('/caja-reembolsos/cobros/crear', methods=['GET', 'POST'], endpoint='crear_cobro_reembolsos')
    @login_required
    def crear_cobro_reembolsos():
        """Crear nuevo cobro en Caja Reembolsos"""
        return _crear_cobro('REEMBOLSOS', 'caja_reembolsos_cobros')
    
    @app.route('/caja-reembolsos/cobros/editar/<int:id>', methods=['GET', 'POST'], endpoint='editar_cobro_reembolsos')
    @login_required
    def editar_cobro_reembolsos(id):
        """Editar cobro existente de Caja Reembolsos"""
        return _editar_cobro(id, 'REEMBOLSOS', 'caja_reembolsos_cobros')
    
    @app.route('/caja-reembolsos/cobros/eliminar/<int:id>', methods=['POST'], endpoint='eliminar_cobro_reembolsos')
    @login_required
    def eliminar_cobro_reembolsos(id):
        """Eliminar cobro de Caja Reembolsos"""
        return _eliminar_cobro(id, 'REEMBOLSOS', 'caja_reembolsos_cobros')
    
    @app.route('/caja-reembolsos/pagos', endpoint='caja_reembolsos_pagos')
    @login_required
    def caja_reembolsos_pagos():
        """Lista de pagos no arqueados de Caja Reembolsos"""
        return _caja_pagos('REEMBOLSOS')
    
    @app.route('/caja-reembolsos/pagos/crear', methods=['GET', 'POST'], endpoint='crear_pago_reembolsos')
    @login_required
    def crear_pago_reembolsos():
        """Crear nuevo pago en Caja Reembolsos"""
        return _crear_pago('REEMBOLSOS', 'caja_reembolsos_pagos')
    
    @app.route('/caja-reembolsos/pagos/editar/<int:id>', methods=['GET', 'POST'], endpoint='editar_pago_reembolsos')
    @login_required
    def editar_pago_reembolsos(id):
        """Editar pago existente de Caja Reembolsos"""
        return _editar_pago(id, 'REEMBOLSOS', 'caja_reembolsos_pagos')
    
    @app.route('/caja-reembolsos/pagos/eliminar/<int:id>', methods=['POST'], endpoint='eliminar_pago_reembolsos')
    @login_required
    def eliminar_pago_reembolsos(id):
        """Eliminar pago de Caja Reembolsos"""
        return _eliminar_pago(id, 'REEMBOLSOS', 'caja_reembolsos_pagos')
    
    @app.route('/caja-reembolsos/arqueo', endpoint='caja_reembolsos_arqueo')
    @login_required
    def caja_reembolsos_arqueo():
        """Página de arqueo de Caja Reembolsos"""
        return _caja_arqueo('REEMBOLSOS', 'Caja Reembolsos')
    
    @app.route('/caja-reembolsos/arqueo/procesar', methods=['POST'], endpoint='procesar_arqueo_reembolsos')
    @login_required
    def procesar_arqueo_reembolsos():
        """Procesar arqueo de Caja Reembolsos"""
        return _procesar_arqueo('REEMBOLSOS', 'caja_reembolsos_arqueo')
    
    @app.route('/caja-reembolsos/arqueo/<int:id>', endpoint='ver_arqueo_detalle_reembolsos')
    @login_required
    def ver_arqueo_detalle_reembolsos(id):
        """Ver detalles de un arqueo de Caja Reembolsos"""
        return _ver_arqueo_detalle(id, 'REEMBOLSOS', 'Caja Reembolsos')


# ========== FUNCIONES HELPER ==========

def _caja_index(tipo_caja, titulo_caja):
    """Función helper para página principal de caja"""
    cobros = db.session.query(CajaCobro).filter_by(arqueado=False, tipo_caja=tipo_caja).order_by(CajaCobro.fecha_albaran.desc()).all()
    pagos = db.session.query(CajaPago).filter_by(arqueado=False, tipo_caja=tipo_caja).order_by(CajaPago.fecha_albaran.desc()).all()
    
    if tipo_caja == 'CAJA':
        # Para caja de contados: suma de entrada_en_caja
        # Asegurarse de que todos los valores sean float y manejar None correctamente
        total_cobros = 0.0
        sys.stdout.write(f"\n=== DEBUG CAJA INDEX ===\n")
        sys.stdout.write(f"Tipo caja: {tipo_caja}\n")
        sys.stdout.write(f"Cobros encontrados: {len(cobros)}\n")
        sys.stdout.flush()
        for c in cobros:
            # Asegurarse de acceder correctamente al atributo
            valor_entrada = getattr(c, 'entrada_en_caja', None)
            valor_iva = getattr(c, 'iva', None)
            if valor_entrada is None:
                valor_entrada = 0.0
            sys.stdout.write(f"Cobro ID {c.id}: Expedición={c.expedicion}, entrada_en_caja={valor_entrada}, iva={valor_iva}, tipo_entrada={type(valor_entrada)}\n")
            sys.stdout.flush()
            total_cobros += float(valor_entrada)
        sys.stdout.write(f"Total calculado: {total_cobros}\n")
        sys.stdout.write(f"=== FIN DEBUG ===\n\n")
        sys.stdout.flush()
    else:
        # Para reembolsos: la comisión suma
        total_cobros = sum(
            float(c.reembolso or 0.0) + float(c.comision_reembolso or 0.0) + float(c.portes_pagados or 0.0) + float(c.portes_debidos or 0.0) + float(c.iva or 0.0)
            for c in cobros
        )
    total_pagos = sum(float(p.base or 0.0) + float(p.iva or 0.0) for p in pagos)
    diferencia = total_cobros - total_pagos
    
    return render_template('caja/index.html', 
                         cobros=cobros, 
                         pagos=pagos,
                         total_cobros=total_cobros,
                         total_pagos=total_pagos,
                         diferencia=diferencia,
                         tipo_caja=tipo_caja,
                         titulo_caja=titulo_caja)

def _caja_cobros(tipo_caja):
    """Función helper para lista de cobros"""
    cobros = db.session.query(CajaCobro).filter_by(arqueado=False, tipo_caja=tipo_caja).order_by(CajaCobro.fecha_albaran.desc()).all()
    
    # Calcular total según el tipo de caja
    if tipo_caja == 'CAJA':
        # Para caja de contados: suma de entrada_en_caja
        # Asegurarse de que todos los valores sean float y manejar None correctamente
        total_cobros = 0.0
        for c in cobros:
            valor = c.entrada_en_caja
            if valor is None:
                valor = 0.0
            total_cobros += float(valor)
    else:
        # Para reembolsos: suma de todos los conceptos - usar EXACTAMENTE el mismo orden que en el template
        total_cobros = sum(
            float(c.reembolso or 0.0) + float(c.comision_reembolso or 0.0) + float(c.portes_pagados or 0.0) + float(c.portes_debidos or 0.0) + float(c.iva or 0.0)
            for c in cobros
        )
    
    return render_template('caja/cobros.html', cobros=cobros, tipo_caja=tipo_caja, total_cobros=total_cobros)

def _crear_cobro(tipo_caja, redirect_route):
    """Función helper para crear cobro"""
    if request.method == 'POST':
        try:
            fecha_str = request.form.get('fecha_albaran')
            fecha_albaran = datetime.strptime(fecha_str, '%Y-%m-%d').date() if fecha_str else date.today()
            
            cobro = CajaCobro(
                fecha_albaran=fecha_albaran,
                expedicion=request.form.get('expedicion', ''),
                agencia=request.form.get('agencia', ''),
                remitente=request.form.get('remitente', ''),
                poblacion_origen=request.form.get('poblacion_origen', ''),
                destinatario=request.form.get('destinatario', ''),
                poblacion_destino=request.form.get('poblacion_destino', ''),
                observaciones=request.form.get('observaciones', ''),
                reembolso=float(request.form.get('reembolso', 0) or 0),
                comision_reembolso=float(request.form.get('comision_reembolso', 0) or 0),
                portes_pagados=float(request.form.get('portes_pagados', 0) or 0),
                portes_debidos=float(request.form.get('portes_debidos', 0) or 0),
                iva=float(request.form.get('iva', 0) or 0),
                entrada_en_caja=float(request.form.get('entrada_en_caja', 0) or 0) if tipo_caja == 'CAJA' else 0.0,
                es_factura=request.form.get('es_factura') == 'on',
                tipo_caja=tipo_caja
            )
            print(f"\n=== DEBUG CREAR COBRO ===")
            print(f"Tipo caja: {tipo_caja}")
            print(f"Valor entrada_en_caja del form: {request.form.get('entrada_en_caja', 0)}")
            print(f"Valor entrada_en_caja guardado: {cobro.entrada_en_caja}")
            print(f"Valor IVA guardado: {cobro.iva}")
            print(f"=== FIN DEBUG CREAR COBRO ===\n")
            db.session.add(cobro)
            db.session.commit()
            flash('Cobro creado correctamente', 'success')
            return redirect(url_for(redirect_route))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear cobro: {str(e)}', 'error')
    
    return render_template('caja/crear_cobro.html', tipo_caja=tipo_caja)

def _editar_cobro(id, tipo_caja, redirect_route):
    """Función helper para editar cobro"""
    cobro = db.session.query(CajaCobro).filter_by(id=id, tipo_caja=tipo_caja).first()
    if not cobro:
        flash('Cobro no encontrado', 'error')
        return redirect(url_for(redirect_route))
    if cobro.arqueado:
        flash('No se puede editar un cobro que ya ha sido arqueado', 'error')
        return redirect(url_for(redirect_route))
    
    if request.method == 'POST':
        try:
            fecha_str = request.form.get('fecha_albaran')
            if fecha_str:
                cobro.fecha_albaran = datetime.strptime(fecha_str, '%Y-%m-%d').date()
            
            cobro.expedicion = request.form.get('expedicion', '')
            cobro.agencia = request.form.get('agencia', '')
            cobro.remitente = request.form.get('remitente', '')
            cobro.poblacion_origen = request.form.get('poblacion_origen', '')
            cobro.destinatario = request.form.get('destinatario', '')
            cobro.poblacion_destino = request.form.get('poblacion_destino', '')
            cobro.observaciones = request.form.get('observaciones', '')
            cobro.reembolso = float(request.form.get('reembolso', 0) or 0)
            cobro.comision_reembolso = float(request.form.get('comision_reembolso', 0) or 0)
            cobro.portes_pagados = float(request.form.get('portes_pagados', 0) or 0)
            cobro.portes_debidos = float(request.form.get('portes_debidos', 0) or 0)
            cobro.iva = float(request.form.get('iva', 0) or 0)
            if tipo_caja == 'CAJA':
                cobro.entrada_en_caja = float(request.form.get('entrada_en_caja', 0) or 0)
            cobro.es_factura = request.form.get('es_factura') == 'on'
            
            db.session.commit()
            flash('Cobro actualizado correctamente', 'success')
            return redirect(url_for(redirect_route))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar cobro: {str(e)}', 'error')
    
    return render_template('caja/editar_cobro.html', cobro=cobro, tipo_caja=tipo_caja)

def _eliminar_cobro(id, tipo_caja, redirect_route):
    """Función helper para eliminar cobro"""
    cobro = db.session.query(CajaCobro).filter_by(id=id, tipo_caja=tipo_caja).first()
    if not cobro:
        flash('Cobro no encontrado', 'error')
    elif cobro.arqueado:
        flash('No se puede eliminar un cobro que ya ha sido arqueado', 'error')
    else:
        db.session.delete(cobro)
        db.session.commit()
        flash('Cobro eliminado correctamente', 'success')
    return redirect(url_for(redirect_route))

def _caja_pagos(tipo_caja):
    """Función helper para lista de pagos"""
    pagos = db.session.query(CajaPago).filter_by(arqueado=False, tipo_caja=tipo_caja).order_by(CajaPago.fecha_albaran.desc()).all()
    
    # Calcular total: suma de base + iva
    total_pagos = sum(p.base + p.iva for p in pagos)
    
    return render_template('caja/pagos.html', pagos=pagos, tipo_caja=tipo_caja, total_pagos=total_pagos)

def _crear_pago(tipo_caja, redirect_route):
    """Función helper para crear pago"""
    if request.method == 'POST':
        try:
            fecha_str = request.form.get('fecha_albaran')
            fecha_albaran = datetime.strptime(fecha_str, '%Y-%m-%d').date() if fecha_str else date.today()
            
            pago = CajaPago(
                fecha_albaran=fecha_albaran,
                albaran=request.form.get('albaran', ''),
                observaciones=request.form.get('observaciones', ''),
                base=float(request.form.get('base', 0) or 0),
                iva=float(request.form.get('iva', 0) or 0),
                es_factura=request.form.get('es_factura') == 'on',
                tipo_caja=tipo_caja
            )
            db.session.add(pago)
            db.session.commit()
            flash('Pago creado correctamente', 'success')
            return redirect(url_for(redirect_route))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear pago: {str(e)}', 'error')
    
    return render_template('caja/crear_pago.html', tipo_caja=tipo_caja)

def _editar_pago(id, tipo_caja, redirect_route):
    """Función helper para editar pago"""
    pago = db.session.query(CajaPago).filter_by(id=id, tipo_caja=tipo_caja).first()
    if not pago:
        flash('Pago no encontrado', 'error')
        return redirect(url_for(redirect_route))
    if pago.arqueado:
        flash('No se puede editar un pago que ya ha sido arqueado', 'error')
        return redirect(url_for(redirect_route))
    
    if request.method == 'POST':
        try:
            fecha_str = request.form.get('fecha_albaran')
            if fecha_str:
                pago.fecha_albaran = datetime.strptime(fecha_str, '%Y-%m-%d').date()
            
            pago.albaran = request.form.get('albaran', '')
            pago.observaciones = request.form.get('observaciones', '')
            pago.base = float(request.form.get('base', 0) or 0)
            pago.iva = float(request.form.get('iva', 0) or 0)
            pago.es_factura = request.form.get('es_factura') == 'on'
            
            db.session.commit()
            flash('Pago actualizado correctamente', 'success')
            return redirect(url_for(redirect_route))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar pago: {str(e)}', 'error')
    
    return render_template('caja/editar_pago.html', pago=pago, tipo_caja=tipo_caja)

def _eliminar_pago(id, tipo_caja, redirect_route):
    """Función helper para eliminar pago"""
    pago = db.session.query(CajaPago).filter_by(id=id, tipo_caja=tipo_caja).first()
    if not pago:
        flash('Pago no encontrado', 'error')
    elif pago.arqueado:
        flash('No se puede eliminar un pago que ya ha sido arqueado', 'error')
    else:
        db.session.delete(pago)
        db.session.commit()
        flash('Pago eliminado correctamente', 'success')
    return redirect(url_for(redirect_route))

def _caja_arqueo(tipo_caja, titulo_caja):
    """Función helper para página de arqueo"""
    cobros = db.session.query(CajaCobro).filter_by(arqueado=False, tipo_caja=tipo_caja).all()
    pagos = db.session.query(CajaPago).filter_by(arqueado=False, tipo_caja=tipo_caja).all()
    
    if tipo_caja == 'CAJA':
        # Para caja de contados: suma de entrada_en_caja
        # Asegurarse de que todos los valores sean float y manejar None correctamente
        total_cobros = 0.0
        for c in cobros:
            valor = c.entrada_en_caja
            if valor is None:
                valor = 0.0
            total_cobros += float(valor)
    else:
        # Para reembolsos: la comisión suma - usar EXACTAMENTE el mismo orden que en el template
        total_cobros = sum(
            float(c.reembolso or 0.0) + float(c.comision_reembolso or 0.0) + float(c.portes_pagados or 0.0) + float(c.portes_debidos or 0.0) + float(c.iva or 0.0)
            for c in cobros
        )
    total_pagos = sum(float(p.base or 0.0) + float(p.iva or 0.0) for p in pagos)
    diferencia = total_cobros - total_pagos
    
    historial = db.session.query(CajaArqueo).filter_by(tipo_caja=tipo_caja).order_by(CajaArqueo.fecha_arqueo.desc()).limit(20).all()
    
    return render_template('caja/arqueo.html', 
                         cobros=cobros, 
                         pagos=pagos,
                         total_cobros=total_cobros,
                         total_pagos=total_pagos,
                         diferencia=diferencia,
                         historial=historial,
                         tipo_caja=tipo_caja,
                         titulo_caja=titulo_caja)

def _procesar_arqueo(tipo_caja, redirect_route):
    """Función helper para procesar arqueo"""
    try:
        entrega_efectivo = float(request.form.get('entrega_efectivo', 0) or 0)
        responsable = request.form.get('responsable', '')
        observaciones = request.form.get('observaciones', '')
        
        cobros = db.session.query(CajaCobro).filter_by(arqueado=False, tipo_caja=tipo_caja).all()
        pagos = db.session.query(CajaPago).filter_by(arqueado=False, tipo_caja=tipo_caja).all()
        
        if tipo_caja == 'CAJA':
            # Para caja de contados: suma de entrada_en_caja
            total_cobros = sum(float(c.entrada_en_caja or 0.0) for c in cobros)
        else:
            # Para reembolsos: la comisión suma - usar EXACTAMENTE el mismo orden que en el template
            total_cobros = sum(
                float(c.reembolso or 0.0) + float(c.comision_reembolso or 0.0) + float(c.portes_pagados or 0.0) + float(c.portes_debidos or 0.0) + float(c.iva or 0.0)
                for c in cobros
            )
        total_pagos = sum(float(p.base or 0.0) + float(p.iva or 0.0) for p in pagos)
        diferencia = total_cobros - total_pagos
        
        if abs(diferencia - entrega_efectivo) > 0.01:
            flash(f'El arqueo no cuadra. Diferencia calculada: {diferencia:.2f}€, Entrega indicada: {entrega_efectivo:.2f}€. La entrega debe ser igual a la diferencia.', 'error')
            return redirect(url_for(redirect_route))
        
        if not cobros and not pagos:
            flash('No hay cobros ni pagos pendientes para arquear', 'error')
            return redirect(url_for(redirect_route))
        
        fecha_arqueo = datetime.now()
        arqueo = CajaArqueo(
            fecha_arqueo=fecha_arqueo,
            usuario=current_user.username,
            total_cobros=total_cobros,
            total_pagos=total_pagos,
            diferencia=diferencia,
            entrega_efectivo=entrega_efectivo,
            responsable=responsable,
            observaciones=observaciones,
            tipo_caja=tipo_caja
        )
        db.session.add(arqueo)
        db.session.flush()
        
        for cobro in cobros:
            cobro.arqueado = True
            cobro.fecha_arqueo = fecha_arqueo
            cobro.arqueo_id = arqueo.id
        
        for pago in pagos:
            pago.arqueado = True
            pago.fecha_arqueo = fecha_arqueo
            pago.arqueo_id = arqueo.id
        
        db.session.commit()
        flash(f'Arqueo procesado correctamente. Se marcaron {len(cobros)} cobros y {len(pagos)} pagos como arqueados.', 'success')
        return redirect(url_for(redirect_route))
        
    except ValueError as e:
        db.session.rollback()
        flash(f'Error de validación: {str(e)}', 'error')
        return redirect(url_for(redirect_route))
    except Exception as e:
        db.session.rollback()
        import traceback
        error_details = traceback.format_exc()
        print(f"Error al procesar arqueo: {error_details}")
        flash(f'Error al procesar arqueo: {str(e)}', 'error')
        return redirect(url_for(redirect_route))

def _ver_arqueo_detalle(id, tipo_caja, titulo_caja):
    """Función helper para ver detalles de un arqueo"""
    arqueo = db.session.query(CajaArqueo).filter_by(id=id, tipo_caja=tipo_caja).first()
    if not arqueo:
        flash('Arqueo no encontrado', 'error')
        if tipo_caja == 'CAJA':
            return redirect(url_for('caja_arqueo'))
        else:
            return redirect(url_for('caja_reembolsos_arqueo'))
    
    # Obtener cobros y pagos asociados a este arqueo
    cobros = db.session.query(CajaCobro).filter_by(arqueo_id=id, tipo_caja=tipo_caja).order_by(CajaCobro.fecha_albaran.desc()).all()
    pagos = db.session.query(CajaPago).filter_by(arqueo_id=id, tipo_caja=tipo_caja).order_by(CajaPago.fecha_albaran.desc()).all()
    
    return render_template('caja/arqueo_detalle.html',
                         arqueo=arqueo,
                         cobros=cobros,
                         pagos=pagos,
                         tipo_caja=tipo_caja,
                         titulo_caja=titulo_caja)
