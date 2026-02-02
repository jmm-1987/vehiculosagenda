from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base
from flask import g, has_request_context
import logging

# Configurar logging para detectar problemas
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

engine = create_engine('sqlite:///database/VEHICULOS.db',
connect_args={'check_same_thread': False})

Session = sessionmaker(bind=engine)
Base = declarative_base()

class SessionProxy:
    """
    Proxy para la sesión de base de datos que obtiene la sesión del request actual.
    Permite usar db.session como antes pero con sesiones por request.
    """
    def __getattr__(self, name):
        if has_request_context():
            if 'db_session' not in g:
                g.db_session = Session()
                logger.info("Nueva sesión de BD creada para el request")
            return getattr(g.db_session, name)
        else:
            # Fuera de contexto de request (ej: scripts, inicialización)
            # Crear una sesión temporal
            if not hasattr(self, '_temp_session'):
                self._temp_session = Session()
                logger.warning("Sesión temporal creada fuera de contexto de request")
            return getattr(self._temp_session, name)
    
    def __call__(self, *args, **kwargs):
        """Permite usar db.session() como función"""
        if has_request_context():
            if 'db_session' not in g:
                g.db_session = Session()
            return g.db_session
        else:
            if not hasattr(self, '_temp_session'):
                self._temp_session = Session()
            return self._temp_session

def get_session():
    """
    Obtiene o crea una sesión de base de datos para el request actual.
    Usa Flask's g para almacenar la sesión por request.
    """
    if has_request_context():
        if 'db_session' not in g:
            g.db_session = Session()
            logger.info("Nueva sesión de BD creada para el request")
        return g.db_session
    else:
        # Fuera de contexto de request
        session = Session()
        logger.warning("Sesión creada fuera de contexto de request")
        return session

def close_session(error=None):
    """
    Cierra la sesión de base de datos al final del request.
    Hace commit automático si no hay errores y hay cambios pendientes, rollback si hay errores.
    """
    if not has_request_context():
        return
    
    session = g.pop('db_session', None)
    if session is not None:
        try:
            if error is None:
                # Solo hacer commit si hay cambios pendientes y la sesión está activa
                if session.is_active:
                    # Verificar si hay objetos nuevos o modificados
                    if session.new or session.dirty or session.deleted:
                        try:
                            session.commit()
                            logger.info("Sesión de BD cerrada con commit automático exitoso")
                        except Exception as commit_error:
                            # Si el commit falla (ej: ya se hizo commit), hacer rollback
                            logger.warning(f"Error en commit automático (posible commit previo): {commit_error}")
                            try:
                                session.rollback()
                            except:
                                pass
                    else:
                        logger.debug("Sesión de BD cerrada sin cambios pendientes")
                else:
                    logger.debug("Sesión de BD ya estaba cerrada o inactiva")
            else:
                session.rollback()
                logger.warning(f"Sesión de BD cerrada con rollback debido a error: {error}")
        except Exception as e:
            logger.error(f"Error al cerrar sesión de BD: {e}")
            try:
                session.rollback()
            except:
                pass
        finally:
            try:
                session.close()
            except:
                pass

# Crear el proxy de sesión para compatibilidad con código existente
session = SessionProxy()

# Utilidad: asegurar columnas en SQLite sin migraciones
def ensure_column_exists(table_name: str, column_name: str, column_type_sql: str, default_value: str = None) -> None:
    """
    Añade una columna a una tabla SQLite si no existe.
    Si se añade o está a NULL, opcionalmente asigna un valor por defecto a filas existentes.
    """
    try:
        with engine.connect() as conn:
            # Verificar que la tabla existe
            tables_check = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name=:table_name"), {"table_name": table_name})
            if not tables_check.fetchone():
                # La tabla no existe, se creará automáticamente con SQLAlchemy
                return
            
            # Consultar esquema actual
            pragma = conn.execute(text(f"PRAGMA table_info({table_name})"))
            columns = [row[1] for row in pragma.fetchall()]
            if column_name not in columns:
                # Añadir la columna
                if default_value is not None:
                    # Para valores booleanos, no usar comillas
                    if isinstance(default_value, bool) or (isinstance(default_value, int) and default_value in [0, 1]):
                        conn.execute(text(
                            f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type_sql} DEFAULT {default_value}"
                        ))
                    else:
                        conn.execute(text(
                            f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type_sql} DEFAULT '{default_value}'"
                        ))
                else:
                    conn.execute(text(
                        f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type_sql}"
                    ))
                conn.commit()
            # Rellenar valores nulos con el default si procede
            if default_value is not None:
                try:
                    # Para valores booleanos, no usar comillas
                    if isinstance(default_value, bool) or (isinstance(default_value, int) and default_value in [0, 1]):
                        conn.execute(text(
                            f"UPDATE {table_name} SET {column_name} = {default_value} WHERE {column_name} IS NULL"
                        ))
                    else:
                        conn.execute(text(
                            f"UPDATE {table_name} SET {column_name} = '{default_value}' WHERE {column_name} IS NULL"
                        ))
                    conn.commit()
                except Exception as e:
                    print(f"Error actualizando valores por defecto en {table_name}.{column_name}: {e}")
    except Exception as e:
        # Mostrar el error para debugging pero no interrumpir el arranque
        print(f"Error añadiendo columna {column_name} a {table_name}: {e}")