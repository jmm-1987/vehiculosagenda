"""
Migración para garantizar unicidad de numero_presupuesto.

Qué hace:
1) Detecta duplicados de numero_presupuesto en la tabla presupuesto.
2) Mantiene el primer registro (menor id) y reasigna duplicados al siguiente
   número correlativo libre.
3) Si existen valores legacy con sufijo "-DUP", también los normaliza a números.
3) Crea un índice único sobre numero_presupuesto.
"""
import os
import sqlite3

DB_PATH = 'database/VEHICULOS.db'


def main():
    if not os.path.exists(DB_PATH):
        print(f"Error: No se encontró la base de datos en {DB_PATH}")
        raise SystemExit(1)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # 1) Cargar todos los números para calcular siguiente correlativo libre
        cursor.execute("""
            SELECT numero_presupuesto
            FROM presupuesto
            WHERE numero_presupuesto IS NOT NULL AND TRIM(numero_presupuesto) <> ''
        """)
        usados_raw = [row[0].strip() for row in cursor.fetchall()]
        usados_numericos = {int(v) for v in usados_raw if v.isdigit()}
        siguiente_num = (max(usados_numericos) + 1) if usados_numericos else 1

        # 2) Buscar números duplicados (ignorar nulos/vacíos)
        cursor.execute("""
            SELECT numero_presupuesto, COUNT(*)
            FROM presupuesto
            WHERE numero_presupuesto IS NOT NULL AND TRIM(numero_presupuesto) <> ''
            GROUP BY numero_presupuesto
            HAVING COUNT(*) > 1
        """)
        duplicados = cursor.fetchall()

        if duplicados:
            print(f"Se encontraron {len(duplicados)} números de presupuesto duplicados.")
        else:
            print("No se encontraron números de presupuesto duplicados.")

        # 3) Reasignar duplicados (excepto el primer ID) al siguiente número libre
        for numero, _ in duplicados:
            cursor.execute("""
                SELECT id
                FROM presupuesto
                WHERE numero_presupuesto = ?
                ORDER BY id ASC
            """, (numero,))
            ids = [row[0] for row in cursor.fetchall()]

            # Mantener el primero, reasignar el resto
            for dup_id in ids[1:]:
                while siguiente_num in usados_numericos:
                    siguiente_num += 1
                nuevo_numero = str(siguiente_num)
                usados_numericos.add(siguiente_num)
                siguiente_num += 1
                cursor.execute("""
                    UPDATE presupuesto
                    SET numero_presupuesto = ?
                    WHERE id = ?
                """, (nuevo_numero, dup_id))
                print(f"ID {dup_id}: {numero} -> {nuevo_numero}")

        # 4) Normalizar valores legacy tipo "123-DUP456" a número correlativo libre
        cursor.execute("""
            SELECT id, numero_presupuesto
            FROM presupuesto
            WHERE numero_presupuesto LIKE '%-DUP%'
        """)
        legacy_dup = cursor.fetchall()
        for reg_id, valor_antiguo in legacy_dup:
            while siguiente_num in usados_numericos:
                siguiente_num += 1
            nuevo_numero = str(siguiente_num)
            usados_numericos.add(siguiente_num)
            siguiente_num += 1
            cursor.execute("""
                UPDATE presupuesto
                SET numero_presupuesto = ?
                WHERE id = ?
            """, (nuevo_numero, reg_id))
            print(f"ID {reg_id}: {valor_antiguo} -> {nuevo_numero}")

        # 5) Crear índice único si no existe
        cursor.execute("""
            CREATE UNIQUE INDEX IF NOT EXISTS ux_presupuesto_numero_presupuesto
            ON presupuesto(numero_presupuesto)
        """)

        conn.commit()
        print("[OK] Migración completada: unicidad de numero_presupuesto garantizada.")
    except Exception as e:
        conn.rollback()
        print(f"Error durante la migración: {e}")
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()

