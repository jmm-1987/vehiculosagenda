"""
Script de migración para agregar columnas bultos, kg y medidas a la tabla presupuesto
Ejecutar este script una vez para agregar las columnas necesarias
"""
import sqlite3
import os

# Ruta a la base de datos
db_path = 'database/VEHICULOS.db'

if not os.path.exists(db_path):
    print(f"Error: No se encontró la base de datos en {db_path}")
    exit(1)

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Verificar si las columnas ya existen
    cursor.execute("PRAGMA table_info(presupuesto)")
    columns = [row[1] for row in cursor.fetchall()]
    
    print("Columnas actuales en presupuesto:", columns)
    
    # Agregar columnas si no existen
    if 'bultos' not in columns:
        cursor.execute("ALTER TABLE presupuesto ADD COLUMN bultos VARCHAR(50) DEFAULT ''")
        print("[OK] Columna 'bultos' agregada")
    else:
        print("[OK] Columna 'bultos' ya existe")
    
    if 'kg' not in columns:
        cursor.execute("ALTER TABLE presupuesto ADD COLUMN kg VARCHAR(50) DEFAULT ''")
        print("[OK] Columna 'kg' agregada")
    else:
        print("[OK] Columna 'kg' ya existe")
    
    if 'medidas' not in columns:
        cursor.execute("ALTER TABLE presupuesto ADD COLUMN medidas VARCHAR(200) DEFAULT ''")
        print("[OK] Columna 'medidas' agregada")
    else:
        print("[OK] Columna 'medidas' ya existe")
    
    conn.commit()
    conn.close()
    
    print("\n[OK] Migracion completada exitosamente!")
    
except Exception as e:
    print(f"Error durante la migración: {e}")
    if conn:
        conn.rollback()
        conn.close()
    exit(1)

