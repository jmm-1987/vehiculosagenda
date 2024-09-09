import db
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy import DateTime, Date


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
