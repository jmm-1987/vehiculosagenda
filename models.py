import db
from sqlalchemy import Column, Integer, String, ForeignKey,Boolean
from sqlalchemy import DateTime, Date
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
