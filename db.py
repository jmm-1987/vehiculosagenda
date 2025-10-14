from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base

engine = create_engine('sqlite:///database/VEHICULOS.db',
connect_args={'check_same_thread': False})


Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

# Utilidad: asegurar columnas en SQLite sin migraciones
def ensure_column_exists(table_name: str, column_name: str, column_type_sql: str, default_value: str = None) -> None:
    """
    Añade una columna a una tabla SQLite si no existe.
    Si se añade o está a NULL, opcionalmente asigna un valor por defecto a filas existentes.
    """
    try:
        with engine.connect() as conn:
            # Consultar esquema actual
            pragma = conn.execute(f"PRAGMA table_info({table_name})")
            columns = [row[1] for row in pragma.fetchall()]
            if column_name not in columns:
                # Añadir la columna
                if default_value is not None:
                    conn.execute(
                        f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type_sql} DEFAULT '{default_value}'"
                    )
                else:
                    conn.execute(
                        f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type_sql}"
                    )
            # Rellenar valores nulos con el default si procede
            if default_value is not None:
                try:
                    conn.execute(
                        f"UPDATE {table_name} SET {column_name} = '{default_value}' WHERE {column_name} IS NULL"
                    )
                except Exception:
                    pass
    except Exception:
        # No interrumpir el arranque por un error no crítico
        pass