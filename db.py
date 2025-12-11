from sqlalchemy import create_engine, text
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