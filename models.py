import db
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Float
from sqlalchemy import DateTime, Date
from sqlalchemy.orm import relationship
from flask_login import UserMixin


class Usuario(UserMixin, db.Base):
    __tablename__ = "usuario"
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True)
    password = Column(String(100))

    def __init__(self, username, password):
        self.username = username
        self.password = password


class Vehiculo(db.Base):
    __tablename__ = "vehiculo"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    matricula = Column(String(200), nullable=False)
    alias = Column(String(200), nullable=False)
    tipo = Column(String(20))
    doc_ficha = Column(String(200))
    doc_permiso = Column(String(200))
    activo = Column(Boolean, default=False)


    def __init__(self, matricula, alias, tipo, doc_ficha="", doc_permiso ="", activo= True):
        self.matricula = matricula
        self.alias = alias
        self.tipo = tipo
        self.doc_ficha = doc_ficha
        self.doc_permiso = doc_permiso
        self.activo = activo


    def __str__(self):
        return "Vehículo {}: {} ({})".format(self.id, self.matricula, self.alias)

class Transpaleta(db.Base):
    __tablename__ = "transpaleta"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    alias = Column(String(200), nullable=False)
    marca = Column(String(200), nullable=False)
    modelo = Column(String(200), nullable=False )
    bastidor = Column(String(200))
    asignada = Column(String(200))
    activo = Column(Boolean, default=False)


    def __init__(self, alias, marca, modelo, bastidor, asignada = None, activo= True):
        self.alias = alias
        self.marca = marca
        self.modelo = modelo
        self.bastidor= bastidor
        if asignada:
            self.asignada = asignada
        else:
            self.asignada = None
        self.activo = activo

class Itv(db.Base):
    __tablename__ = "itv"
    id = Column(Integer, primary_key=True)
    matricula = Column(String(200), ForeignKey('vehiculo.matricula'),nullable=False )
    fecha_itv = Column(DateTime, nullable=False)
    venc_itv = Column(DateTime, nullable=False)
    cita_itv = Column(DateTime)
    obs_itv = Column(String(200), default=None)
    nombre_doc = Column(String(200))
    activo = Column(Boolean, default=False)

    def __init__(self, matricula, fecha_itv, venc_itv, cita_itv=None, obs_itv=None, nombre_doc="", activo= True):
        self.matricula = matricula
        self.fecha_itv = fecha_itv
        self.venc_itv = venc_itv
        if cita_itv:
            self.cita_itv = cita_itv
        else:
            self.cita_itv = None
        self.obs_itv = obs_itv
        self.nombre_doc = nombre_doc
        self.activo = activo

class Seguro(db.Base):
    __tablename__ = "seguro"
    id = Column(Integer, primary_key=True)
    matricula = Column(String(200), ForeignKey('vehiculo.matricula'),nullable=False )
    venc_seguro = Column(DateTime, nullable=False)
    cia_seguro = Column(String(200), nullable=False)
    cob_seguro = Column(String(200))
    obs_seguro = Column(String(200))
    fra_seguro = Column(String(200))
    pri_seguro = Column(String(200))
    nombre_doc = Column(String(200))
    activo = Column(Boolean, default=False)

    def __init__(self, matricula, venc_seguro, cia_seguro, cob_seguro, obs_seguro, fra_seguro, pri_seguro, nombre_doc="", activo= True):
        self.matricula = matricula
        self.venc_seguro = venc_seguro
        self.cia_seguro = cia_seguro
        self.cob_seguro = cob_seguro
        self.obs_seguro = obs_seguro
        self.fra_seguro = fra_seguro
        self.pri_seguro = pri_seguro
        self.nombre_doc = nombre_doc
        self.activo = activo

class Tacografo(db.Base):
    __tablename__ = "tacografo"
    id = Column(Integer, primary_key=True)
    matricula = Column(String(200), ForeignKey('vehiculo.matricula'),nullable=False )
    rev_tacografo = Column(DateTime, nullable=False)
    venc_tacografo = Column(DateTime, nullable=False)
    obs_tacografo = Column(String(200))
    nombre_doc = Column(String(100))
    ruta_doc = Column(String(200))
    activo = Column(Boolean, default=False)

    def __init__(self, matricula, rev_tacografo, venc_tacografo, obs_tacografo, nombre_doc="", activo=True):
        self.matricula = matricula
        self.rev_tacografo = rev_tacografo
        self.venc_tacografo = venc_tacografo
        self.obs_tacografo = obs_tacografo
        self.nombre_doc = nombre_doc
        self.activo = activo

class Rodaje(db.Base):
    __tablename__ = "rodaje"
    id = Column(Integer, primary_key=True)
    matricula = Column(String(200), ForeignKey('vehiculo.matricula'),nullable=False )
    pago_rodaje = Column(DateTime, nullable=False)
    venc_rodaje = Column(DateTime, nullable=False)
    obs_rodaje = Column(String(200))
    imp_rodaje = Column(String(200), nullable=False)
    nombre_doc = Column(String(200))
    activo = Column(Boolean, default=False)

    def __init__(self, matricula, pago_rodaje, venc_rodaje, imp_rodaje, obs_rodaje=None, nombre_doc="", activo= True):
        self.matricula = matricula
        self.pago_rodaje = pago_rodaje
        self.venc_rodaje = venc_rodaje
        self.obs_rodaje = obs_rodaje
        self.imp_rodaje = imp_rodaje
        self.nombre_doc = nombre_doc
        self.activo = activo


class Extintor(db.Base):
    __tablename__ = "extintor"
    id = Column(Integer, primary_key=True)
    matricula = Column(String(200), ForeignKey('vehiculo.matricula'),nullable=False )
    id_ext = Column(String(200), nullable=False)
    ano_ext = Column(String(200), nullable=False)
    rev_ext = Column(DateTime, nullable=False)
    venc_ret_ext = Column(DateTime, nullable=False)
    venc_ext = Column(DateTime, nullable=False)
    obs_ext = Column(String(200))
    activo = Column(Boolean, default=False)


    def __init__(self, matricula, id_ext, ano_ext, rev_ext,venc_ret_ext,venc_ext,obs_ext=None, activo= True):
        self.matricula = matricula
        self.id_ext = id_ext
        self.ano_ext = ano_ext
        self.rev_ext = rev_ext
        self.venc_ret_ext = venc_ret_ext
        self.venc_ext = venc_ext
        self.obs_ext = obs_ext
        self.activo = activo
class Ticket(db.Base):
    __tablename__ = "ticket"
    id = Column(Integer, primary_key=True)
    matricula = Column(String(200), ForeignKey('vehiculo.matricula'),nullable=False )
    fecha_ticket = Column(DateTime, nullable=False)
    tipo_ticket = Column(String(8))
    kms_ticket = Column(Integer)
    litros_ticket = Column(Integer, nullable=False)
    precio_ticket = Column(Integer, nullable=False)
    precio_litro_ticket = Column(Integer)
    obs_ticket = Column(String(200))
    facturado = Column(Boolean, default=False)
    marcado = Column(Boolean, default=False)


    def __init__(self, matricula,fecha_ticket,tipo_ticket, kms_ticket, litros_ticket, precio_ticket,precio_litro_ticket,obs_ticket,facturado=False, marcado=False):
        self.matricula = matricula
        self.fecha_ticket = fecha_ticket
        self.tipo_ticket = tipo_ticket
        self.kms_ticket = kms_ticket
        self.litros_ticket = litros_ticket
        self.precio_ticket = precio_ticket
        self.precio_litro_ticket = precio_litro_ticket
        self.obs_ticket = obs_ticket
        self.facturado = facturado
        self.marcado = marcado


#Esta clase se usa únicamente para las transpaletas
class Visita(db.Base):
    __tablename__ = "visita"
    id = Column(Integer, primary_key=True)
    alias = Column(String(200), ForeignKey('transpaleta.alias'),nullable=False )
    problema = Column(String(200), nullable=False)
    taller = Column(String(200), nullable=False)
    albaran = Column(String(200))
    trabajos = Column(String(200))
    presupuesto = Column(Integer)
    importe = Column(Integer)
    fecha_visita = Column(DateTime, nullable=False)
    fecha_entrega = Column(DateTime)
    nombre_doc = Column(String(200))
    marcado = Column(Boolean, default=False)
    finalizado = Column(Boolean, default=False)


    def __init__(self, alias,problema, taller, albaran, trabajos,presupuesto,importe,fecha_visita, fecha_entrega=None,nombre_doc="", finalizado=False, marcado=False):
        self.alias = alias
        self.problema = problema
        self.taller = taller
        self.albaran = albaran
        self.trabajos = trabajos
        self.presupuesto = presupuesto
        self.importe = importe
        self.fecha_visita = fecha_visita
        self.fecha_entrega = fecha_entrega
        self.nombre_doc = nombre_doc
        self.finalizado = finalizado
        self.marcado = marcado

class Taller(db.Base):
    __tablename__ = "taller"
    id = Column(Integer, primary_key=True)
    matricula = Column(String(200), ForeignKey('vehiculo.matricula'), nullable=False)
    problema = Column(String(200), nullable=False)
    taller = Column(String(200), nullable=False)
    albaran = Column(String(200))
    trabajos = Column(String(200))
    presupuesto = Column(Integer)
    importe = Column(Integer)
    fecha_visita = Column(DateTime, nullable=False)
    kilometros = Column(Integer)
    fecha_entrega = Column(DateTime)
    nombre_doc = Column(String(200))
    marcado = Column(Boolean, default=False)
    activo = Column(Boolean, default=True)


    def __init__(self, matricula, problema, taller, albaran, trabajos,presupuesto,importe,fecha_visita, kilometros, fecha_entrega=None,nombre_doc="", activo=True, marcado=False):
        self.matricula = matricula
        self.problema = problema
        self.taller = taller
        self.albaran = albaran
        self.trabajos = trabajos
        self.presupuesto = presupuesto
        self.importe = importe
        self.fecha_visita = fecha_visita
        self.kilometros = kilometros
        self.fecha_entrega = fecha_entrega
        self.nombre_doc = nombre_doc
        self.activo = activo
        self.marcado = marcado

class Tarea(db.Base):
    __tablename__ = "tarea"
    id = Column(Integer, primary_key=True)
    titulo = Column(String(20), nullable=False)
    contenido = Column(String(200), nullable=False)
    fecha_alta = Column(DateTime, nullable=False)
    fecha_alerta = Column(Date, nullable=False)
    realizada = Column(Boolean, default=False)
    nombre_doc = Column(String(200))
    usuario = Column(String(20))

    def __init__(self, titulo, contenido, fecha_alta, fecha_alerta, realizada, nombre_doc="", usuario=""):
        self.titulo = titulo
        self.contenido = contenido
        self.fecha_alta = fecha_alta
        self.fecha_alerta = fecha_alerta
        self.realizada = realizada
        self.nombre_doc = nombre_doc
        self.usuario= usuario

class IncidenciaAldipod(db.Base):
    __tablename__ = "incidencia_aldipod"
    id = Column(Integer, primary_key=True)
    fecha = Column(DateTime, nullable=False)
    usuario = Column(String(100))
    cliente = Column(String(100), nullable=False)
    referencia = Column(String(200), nullable=False)
    enlace_imagen = Column(String(500), nullable=False)
    tipo_documento = Column(String(100), nullable=False, default="INCIDENCIA")
    comunicada = Column(Boolean, default=False)
    ubicacion = Column(String(50), nullable=False, default="Mérida")
    observaciones = Column(String(1000))
    
    def __init__(self, fecha, usuario, cliente, referencia, enlace_imagen, tipo_documento="INCIDENCIA", comunicada=False, ubicacion="Mérida", observaciones=None):
        self.fecha = fecha
        self.usuario = usuario
        self.cliente = cliente
        self.referencia = referencia
        self.enlace_imagen = enlace_imagen
        self.tipo_documento = tipo_documento
        self.comunicada = comunicada
        self.ubicacion = ubicacion
        self.observaciones = observaciones


class CajaCobro(db.Base):
    __tablename__ = "caja_cobro"
    id = Column(Integer, primary_key=True)
    fecha_albaran = Column(Date, nullable=False)
    expedicion = Column(String(200))
    agencia = Column(String(200))
    remitente = Column(String(200))
    poblacion_origen = Column(String(200))
    destinatario = Column(String(200))
    poblacion_destino = Column(String(200))
    observaciones = Column(String(500))
    reembolso = Column(Float, default=0.0)
    comision_reembolso = Column(Float, default=0.0)
    portes_pagados = Column(Float, default=0.0)
    portes_debidos = Column(Float, default=0.0)
    iva = Column(Float, default=0.0)
    entrada_en_caja = Column(Float, default=0.0)  # Solo para CAJA, no para REEMBOLSOS
    es_factura = Column(Boolean, default=False)
    arqueado = Column(Boolean, default=False)
    fecha_arqueo = Column(DateTime)
    arqueo_id = Column(Integer, ForeignKey('caja_arqueo.id'))
    tipo_caja = Column(String(20), default='CAJA', nullable=False)  # 'CAJA' o 'REEMBOLSOS'
    
    def __init__(self, fecha_albaran, expedicion="", agencia="", remitente="", poblacion_origen="", 
                 destinatario="", poblacion_destino="", observaciones="", reembolso=0.0, 
                 comision_reembolso=0.0, portes_pagados=0.0, portes_debidos=0.0, iva=0.0, 
                 entrada_en_caja=0.0, es_factura=False, arqueado=False, fecha_arqueo=None, arqueo_id=None, tipo_caja='CAJA'):
        self.fecha_albaran = fecha_albaran
        self.expedicion = expedicion
        self.agencia = agencia
        self.remitente = remitente
        self.poblacion_origen = poblacion_origen
        self.destinatario = destinatario
        self.poblacion_destino = poblacion_destino
        self.observaciones = observaciones
        self.reembolso = reembolso
        self.comision_reembolso = comision_reembolso
        self.portes_pagados = portes_pagados
        self.portes_debidos = portes_debidos
        self.iva = iva
        self.entrada_en_caja = entrada_en_caja
        self.es_factura = es_factura
        self.arqueado = arqueado
        self.fecha_arqueo = fecha_arqueo
        self.arqueo_id = arqueo_id
        self.tipo_caja = tipo_caja


class CajaPago(db.Base):
    __tablename__ = "caja_pago"
    id = Column(Integer, primary_key=True)
    fecha_albaran = Column(Date, nullable=False)
    albaran = Column(String(200))
    observaciones = Column(String(500))
    base = Column(Float, default=0.0)
    iva = Column(Float, default=0.0)
    es_factura = Column(Boolean, default=False)
    arqueado = Column(Boolean, default=False)
    fecha_arqueo = Column(DateTime)
    arqueo_id = Column(Integer, ForeignKey('caja_arqueo.id'))
    tipo_caja = Column(String(20), default='CAJA', nullable=False)  # 'CAJA' o 'REEMBOLSOS'
    
    def __init__(self, fecha_albaran, albaran="", observaciones="", base=0.0, iva=0.0, 
                 es_factura=False, arqueado=False, fecha_arqueo=None, arqueo_id=None, tipo_caja='CAJA'):
        self.fecha_albaran = fecha_albaran
        self.albaran = albaran
        self.observaciones = observaciones
        self.base = base
        self.iva = iva
        self.es_factura = es_factura
        self.arqueado = arqueado
        self.fecha_arqueo = fecha_arqueo
        self.arqueo_id = arqueo_id
        self.tipo_caja = tipo_caja


class CajaArqueo(db.Base):
    __tablename__ = "caja_arqueo"
    id = Column(Integer, primary_key=True)
    fecha_arqueo = Column(DateTime, nullable=False)
    usuario = Column(String(100), nullable=False)
    total_cobros = Column(Float, default=0.0)
    total_pagos = Column(Float, default=0.0)
    diferencia = Column(Float, default=0.0)
    entrega_efectivo = Column(Float, default=0.0)
    responsable = Column(String(200))
    observaciones = Column(String(500))
    tipo_caja = Column(String(20), default='CAJA', nullable=False)  # 'CAJA' o 'REEMBOLSOS'
    
    def __init__(self, fecha_arqueo, usuario, total_cobros=0.0, total_pagos=0.0, diferencia=0.0, 
                 entrega_efectivo=0.0, responsable="", observaciones="", tipo_caja='CAJA'):
        self.fecha_arqueo = fecha_arqueo
        self.usuario = usuario
        self.total_cobros = total_cobros
        self.total_pagos = total_pagos
        self.diferencia = diferencia
        self.entrega_efectivo = entrega_efectivo
        self.responsable = responsable
        self.observaciones = observaciones
        self.tipo_caja = tipo_caja


class ClientePresupuesto(db.Base):
    __tablename__ = "clientes_presupuestos"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(200), nullable=False)
    cif = Column(String(50), nullable=False)
    direccion = Column(String(300), nullable=False)
    poblacion = Column(String(200))
    telefono = Column(String(50))
    email = Column(String(200))
    activo = Column(Boolean, default=True)
    
    def __init__(self, nombre, cif, direccion, poblacion="", telefono="", email="", activo=True):
        self.nombre = nombre
        self.cif = cif
        self.direccion = direccion
        self.poblacion = poblacion
        self.telefono = telefono
        self.email = email
        self.activo = activo
    
    def __str__(self):
        return f"{self.nombre} ({self.cif})"


class Presupuesto(db.Base):
    __tablename__ = "presupuesto"
    id = Column(Integer, primary_key=True)
    numero_presupuesto = Column(String(100), nullable=False, unique=True)
    fecha_presupuesto = Column(DateTime, nullable=False)
    cliente_id = Column(Integer, ForeignKey('clientes_presupuestos.id'), nullable=False)
    cliente = Column(String(200), default='')  # Columna legacy para compatibilidad con BD existente, usar cliente_id
    concepto = Column(String(500))  # Mantener por compatibilidad con BD existente
    bultos = Column(String(50))  # Campo obligatorio en formulario
    kg = Column(String(50))  # Campo obligatorio en formulario
    medidas = Column(String(200))  # Campo obligatorio en formulario
    importe = Column(Float, default=0.0)
    iva = Column(Float, default=0.0)
    total = Column(Float, default=0.0)
    estado = Column(String(50), default='PENDIENTE')  # PENDIENTE, APROBADO, RECHAZADO
    observaciones = Column(String(1000))
    nombre_doc = Column(String(200))
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, nullable=False)
    usuario_creacion = Column(String(100))
    
    # Relación con ClientePresupuesto (usar cliente_obj para acceder al objeto relacionado)
    cliente_obj = relationship("ClientePresupuesto", backref="presupuestos")
    
    def __init__(self, numero_presupuesto, fecha_presupuesto, cliente_id, concepto="", 
                 bultos="", kg="", medidas="", importe=0.0, iva=0.0, total=0.0, estado='PENDIENTE', observaciones="", 
                 nombre_doc="", activo=True, fecha_creacion=None, usuario_creacion=""):
        self.numero_presupuesto = numero_presupuesto
        self.fecha_presupuesto = fecha_presupuesto
        self.cliente_id = cliente_id
        self.cliente = ''  # Valor por defecto para columna legacy (compatibilidad con BD)
        self.concepto = concepto  # Mantener por compatibilidad
        self.bultos = bultos
        self.kg = kg
        self.medidas = medidas
        self.importe = importe
        self.iva = iva
        self.total = total
        self.estado = estado
        self.observaciones = observaciones
        self.nombre_doc = nombre_doc
        self.activo = activo
        self.fecha_creacion = fecha_creacion
        self.usuario_creacion = usuario_creacion


class FacturaProforma(db.Base):
    __tablename__ = "factura_proforma"
    id = Column(Integer, primary_key=True)
    numero_factura_proforma = Column(String(100), nullable=False)  # Formato: aaaa + contador
    fecha_factura_proforma = Column(DateTime, nullable=False)
    presupuesto_id = Column(Integer, ForeignKey('presupuesto.id'), nullable=False)
    cliente_id = Column(Integer, ForeignKey('clientes_presupuestos.id'), nullable=False)
    bultos = Column(String(50))
    kg = Column(String(50))
    medidas = Column(String(200))
    importe = Column(Float, default=0.0)
    iva = Column(Float, default=0.0)
    total = Column(Float, default=0.0)
    observaciones = Column(String(1000))
    fecha_creacion = Column(DateTime, nullable=False)
    usuario_creacion = Column(String(100))
    
    # Relaciones
    presupuesto_obj = relationship("Presupuesto", backref="facturas_proforma")
    cliente_obj = relationship("ClientePresupuesto", backref="facturas_proforma")
    
    def __init__(self, numero_factura_proforma, fecha_factura_proforma, presupuesto_id, cliente_id,
                 bultos="", kg="", medidas="", importe=0.0, iva=0.0, total=0.0, observaciones="",
                 fecha_creacion=None, usuario_creacion=""):
        self.numero_factura_proforma = numero_factura_proforma
        self.fecha_factura_proforma = fecha_factura_proforma
        self.presupuesto_id = presupuesto_id
        self.cliente_id = cliente_id
        self.bultos = bultos
        self.kg = kg
        self.medidas = medidas
        self.importe = importe
        self.iva = iva
        self.total = total
        self.observaciones = observaciones
        self.fecha_creacion = fecha_creacion
        self.usuario_creacion = usuario_creacion