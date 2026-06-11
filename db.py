from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import NullPool
from flask import g, has_request_context
import logging
import os

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ruta base
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, 'database', 'VEHICULOS.db')

# Asegurar carpeta database
os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)

# Engine SQLite sin pool para evitar QueuePool limit
engine = create_engine(
    f'sqlite:///{DATABASE_PATH}',
    connect_args={
        'check_same_thread': False,
        'timeout': 30
    },
    poolclass=NullPool,
)

Session = sessionmaker(bind=engine)
Base = declarative_base()


class SessionProxy:
    """
    Proxy de sesion para mantener compatibilidad con db.session
    """

    def __getattr__(self, name):
        if has_request_context():
            if 'db_session' not in g:
                g.db_session = Session()
                logger.info("Nueva sesion de BD creada para el request")

            return getattr(g.db_session, name)

        temp_session = Session()

        try:
            return getattr(temp_session, name)
        finally:
            temp_session.close()

    def __call__(self, *args, **kwargs):
        if has_request_context():
            if 'db_session' not in g:
                g.db_session = Session()
                logger.info("Nueva sesion de BD creada para el request")

            return g.db_session

        logger.warning("Sesion temporal creada fuera de contexto request")
        return Session()


def get_session():
    """
    Obtener o crear sesion del request actual
    """

    if has_request_context():
        if 'db_session' not in g:
            g.db_session = Session()
            logger.info("Nueva sesion de BD creada para el request")

        return g.db_session

    logger.warning("Sesion creada fuera de contexto request")
    return Session()


def close_session(error=None):
    """
    Cerrar sesion al terminar request
    """

    if not has_request_context():
        return

    session = g.pop('db_session', None)

    if session is None:
        return

    try:
        if error is not None:
            session.rollback()
            logger.warning(
                f"Sesion de BD cerrada con rollback por error: {error}"
            )
        else:
            try:
                if session.new or session.dirty or session.deleted:
                    session.commit()
                    logger.info(
                        "Sesion de BD cerrada con commit automatico"
                    )
                else:
                    session.rollback()

            except Exception as commit_error:
                logger.error(
                    f"Error commit/rollback sesion: {commit_error}"
                )
                session.rollback()
                raise

    except Exception as e:
        logger.error(f"Error cerrando sesion de BD: {e}")

        try:
            session.rollback()
        except Exception:
            pass

    finally:
        try:
            session.close()
        except Exception:
            pass


session = SessionProxy()


def ensure_column_exists(
    table_name: str,
    column_name: str,
    column_type_sql: str,
    default_value: str = None
) -> None:
    """
    Anade columna SQLite si no existe
    """

    try:
        with engine.connect() as conn:
            tables_check = conn.execute(
                text(
                    "SELECT name FROM sqlite_master "
                    "WHERE type='table' AND name=:table_name"
                ),
                {"table_name": table_name}
            )

            if not tables_check.fetchone():
                return

            pragma = conn.execute(
                text(f"PRAGMA table_info({table_name})")
            )

            columns = [row[1] for row in pragma.fetchall()]

            if column_name not in columns:
                if default_value is not None:
                    if (
                        isinstance(default_value, bool)
                        or (
                            isinstance(default_value, int)
                            and default_value in [0, 1]
                        )
                    ):
                        conn.execute(
                            text(
                                f"ALTER TABLE {table_name} "
                                f"ADD COLUMN {column_name} "
                                f"{column_type_sql} "
                                f"DEFAULT {default_value}"
                            )
                        )
                    else:
                        conn.execute(
                            text(
                                f"ALTER TABLE {table_name} "
                                f"ADD COLUMN {column_name} "
                                f"{column_type_sql} "
                                f"DEFAULT '{default_value}'"
                            )
                        )
                else:
                    conn.execute(
                        text(
                            f"ALTER TABLE {table_name} "
                            f"ADD COLUMN {column_name} "
                            f"{column_type_sql}"
                        )
                    )

                conn.commit()

            if default_value is not None:
                try:
                    if (
                        isinstance(default_value, bool)
                        or (
                            isinstance(default_value, int)
                            and default_value in [0, 1]
                        )
                    ):
                        conn.execute(
                            text(
                                f"UPDATE {table_name} "
                                f"SET {column_name} = {default_value} "
                                f"WHERE {column_name} IS NULL"
                            )
                        )
                    else:
                        conn.execute(
                            text(
                                f"UPDATE {table_name} "
                                f"SET {column_name} = '{default_value}' "
                                f"WHERE {column_name} IS NULL"
                            )
                        )

                    conn.commit()

                except Exception as e:
                    print(
                        f"Error actualizando valores por defecto "
                        f"en {table_name}.{column_name}: {e}"
                    )

    except Exception as e:
        print(
            f"Error anadiendo columna "
            f"{column_name} a {table_name}: {e}"
        )