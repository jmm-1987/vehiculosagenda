-- Import ausencias vacaciones Merida 2026
-- DB SQLite: database/VEHICULOS.db
--
-- PASO A (solo la primera vez, si falla 'duplicate column' ignoralo):
--   ALTER TABLE vacaciones_ausencia ADD COLUMN nota VARCHAR(1000) DEFAULT '';
--
-- PASO B:
--   sqlite3 /ruta/database/VEHICULOS.db < vacaciones/import_vacaciones_ausencias_merida_2026.sql
--
-- Reejecutable: UPSERT por (empleado_id, fecha). Sede = merida.

BEGIN;

CREATE UNIQUE INDEX IF NOT EXISTS uq_vacaciones_ausencia_emp_fecha
  ON vacaciones_ausencia(empleado_id, fecha);

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-04-14', 'ANJ', 'Pide la tarde para acompañar a su mujer pruebas médicas', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'ALEJANDRO ESPINO JIMENEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-13', 'BM', 'Falta todo el día por fiebre', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'ALEJANDRO ESPINO JIMENEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-17', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'ALEJANDRO ESPINO JIMENEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-18', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'ALEJANDRO ESPINO JIMENEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-19', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'ALEJANDRO ESPINO JIMENEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-20', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'ALEJANDRO ESPINO JIMENEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-21', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'ALEJANDRO ESPINO JIMENEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-05-12', 'ANJ', 'Ismael se va a las 8 por pruebas de su mujer', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'ALFREDO ISMAEL CENTENO RICO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-05-15', 'ANJ', 'Pide la tarde por graduación de su hijo', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'ALFREDO ISMAEL CENTENO RICO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-06', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'ALFREDO ISMAEL CENTENO RICO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-07', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'ALFREDO ISMAEL CENTENO RICO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-08', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'ALFREDO ISMAEL CENTENO RICO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-09', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'ALFREDO ISMAEL CENTENO RICO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-10', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'ALFREDO ISMAEL CENTENO RICO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-13', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'ALFREDO ISMAEL CENTENO RICO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-14', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'ALFREDO ISMAEL CENTENO RICO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-15', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'ALFREDO ISMAEL CENTENO RICO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-16', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'ALFREDO ISMAEL CENTENO RICO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-17', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'ALFREDO ISMAEL CENTENO RICO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-20', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'ALONSO MORENO GOMEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-21', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'ALONSO MORENO GOMEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-22', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'ALONSO MORENO GOMEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-23', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'ALONSO MORENO GOMEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-24', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'ALONSO MORENO GOMEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-24', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'ALONSO MORENO GOMEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-25', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'ALONSO MORENO GOMEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-26', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'ALONSO MORENO GOMEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-27', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'ALONSO MORENO GOMEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-28', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'ALONSO MORENO GOMEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-04-21', 'BM', 'El día previo se mareó y este día falta por lo mismo', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'BLANCA GARCIA RUBIO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-05-08', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'BLANCA GARCIA RUBIO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-05-11', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'BLANCA GARCIA RUBIO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-05-12', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'BLANCA GARCIA RUBIO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-05-13', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'BLANCA GARCIA RUBIO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-05-14', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'BLANCA GARCIA RUBIO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-05-15', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'BLANCA GARCIA RUBIO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-05-18', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'BLANCA GARCIA RUBIO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-05-19', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'BLANCA GARCIA RUBIO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-05-20', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'BLANCA GARCIA RUBIO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-06-12', 'OT', 'Pide salir el viernes a las 19h por un concierto fuera. La cubre Alejandro', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'BLANCA GARCIA RUBIO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-06-16', 'AJ', 'Fallecimiento abuela', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'BLANCA GARCIA RUBIO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-06-17', 'AJ', 'Entierro de su abuela', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'BLANCA GARCIA RUBIO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-02-19', 'OT', 'Llega a las 17:00 por urgencia veterinaria con el perro', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'CARMEN MARIA TRINIDAD RAMOS'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-10', 'ANJ', 'Se va a las 21 por fiebre. Cubre Alejandro', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'CARMEN MARIA TRINIDAD RAMOS'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-03', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'CARMEN MARIA TRINIDAD RAMOS'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-04', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'CARMEN MARIA TRINIDAD RAMOS'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-05', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'CARMEN MARIA TRINIDAD RAMOS'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-06', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'CARMEN MARIA TRINIDAD RAMOS'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-07', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'CARMEN MARIA TRINIDAD RAMOS'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-10', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'CARMEN MARIA TRINIDAD RAMOS'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-11', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'CARMEN MARIA TRINIDAD RAMOS'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-12', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'CARMEN MARIA TRINIDAD RAMOS'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-13', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'CARMEN MARIA TRINIDAD RAMOS'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-14', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'CARMEN MARIA TRINIDAD RAMOS'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-04-30', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'DAVID JIMENEZ CALERO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-18', 'OT', 'Tenia que venir este sábado y falta por tener una boda fuera. Víctor estaba de vacaciones', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'DAVID JIMENEZ CALERO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-20', 'ANJ', 'Falta todo el día tras mundial de España. Borrachera', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'DAVID JIMENEZ CALERO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-09-07', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'DAVID JIMENEZ CALERO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-09-08', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'DAVID JIMENEZ CALERO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-09-09', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'DAVID JIMENEZ CALERO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-09-10', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'DAVID JIMENEZ CALERO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-09-11', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'DAVID JIMENEZ CALERO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-09-14', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'DAVID JIMENEZ CALERO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-09-15', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'DAVID JIMENEZ CALERO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-09-16', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'DAVID JIMENEZ CALERO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-09-17', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'DAVID JIMENEZ CALERO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-09-18', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'DAVID JIMENEZ CALERO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-17', 'BM', 'Gastroenteritis. Sí va la noche siguiente', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'DAVID SANCHEZ SANCHEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-24', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'DAVID SANCHEZ SANCHEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-31', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'DAVID SANCHEZ SANCHEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-09-01', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'DAVID SANCHEZ SANCHEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-09-02', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'DAVID SANCHEZ SANCHEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-09-03', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'DAVID SANCHEZ SANCHEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-09-04', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'DAVID SANCHEZ SANCHEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-09-07', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'DAVID SANCHEZ SANCHEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-09-08', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'DAVID SANCHEZ SANCHEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-09-09', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'DAVID SANCHEZ SANCHEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-09-10', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'DAVID SANCHEZ SANCHEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-09-11', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'DAVID SANCHEZ SANCHEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-03-20', 'V', 'Día pedido para feria de Calamonte', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'DIEGO JOSE DELGADO ALVAREZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-10', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'DIEGO JOSE DELGADO ALVAREZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-11', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'DIEGO JOSE DELGADO ALVAREZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-12', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'DIEGO JOSE DELGADO ALVAREZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-13', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'DIEGO JOSE DELGADO ALVAREZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-14', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'DIEGO JOSE DELGADO ALVAREZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-17', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'DIEGO JOSE DELGADO ALVAREZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-18', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'DIEGO JOSE DELGADO ALVAREZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-19', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'DIEGO JOSE DELGADO ALVAREZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-20', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'DIEGO JOSE DELGADO ALVAREZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-21', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'DIEGO JOSE DELGADO ALVAREZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-05-04', 'AJ', 'Fallecimiento suegro', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'FATIMA BONILLA GONZALEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-05-05', 'AJ', 'Fallecimiento suegro', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'FATIMA BONILLA GONZALEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-05-19', 'ANJ', 'Sale a las 9:30 con la niña al médico y no vuelve. Esa semana estaba hasta las 12 ya que estaba de partido', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'FATIMA BONILLA GONZALEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-06-22', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'FATIMA BONILLA GONZALEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-06-23', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'FATIMA BONILLA GONZALEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-06-24', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'FATIMA BONILLA GONZALEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-06-25', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'FATIMA BONILLA GONZALEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-06-26', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'FATIMA BONILLA GONZALEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-06-29', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'FATIMA BONILLA GONZALEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-06-30', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'FATIMA BONILLA GONZALEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-01', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'FATIMA BONILLA GONZALEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-02', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'FATIMA BONILLA GONZALEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-03', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'FATIMA BONILLA GONZALEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-09-11', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'FATIMA BONILLA GONZALEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-01-14', 'BM', 'Se va a las 4:00 por encontrarse mal', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'GABRIEL BONILLA BENITEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-06-05', 'ANJ', 'Se va a las 3 por dolor de espalda', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'GABRIEL BONILLA BENITEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-18', 'BM', 'Se va a las 3 por la barriga', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'GABRIEL BONILLA BENITEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-10', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'GABRIEL BONILLA BENITEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-11', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'GABRIEL BONILLA BENITEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-12', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'GABRIEL BONILLA BENITEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-13', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'GABRIEL BONILLA BENITEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-14', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'GABRIEL BONILLA BENITEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-17', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'GABRIEL BONILLA BENITEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-18', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'GABRIEL BONILLA BENITEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-19', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'GABRIEL BONILLA BENITEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-20', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'GABRIEL BONILLA BENITEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-21', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'GABRIEL BONILLA BENITEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-15', 'ANJ', 'Sale al médico con su mujer de 11 a 13', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'IVAN CASTRO MERINO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-10', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'IVAN CASTRO MERINO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-11', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'IVAN CASTRO MERINO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-12', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'IVAN CASTRO MERINO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-13', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'IVAN CASTRO MERINO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-14', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'IVAN CASTRO MERINO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-17', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'IVAN CASTRO MERINO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-18', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'IVAN CASTRO MERINO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-19', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'IVAN CASTRO MERINO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-20', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'IVAN CASTRO MERINO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-21', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'IVAN CASTRO MERINO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-06-19', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JESUS MIGUEL OTERO MAYORAL'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-20', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JESUS MIGUEL OTERO MAYORAL'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-21', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JESUS MIGUEL OTERO MAYORAL'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-22', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JESUS MIGUEL OTERO MAYORAL'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-23', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JESUS MIGUEL OTERO MAYORAL'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-24', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JESUS MIGUEL OTERO MAYORAL'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-27', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JESUS MIGUEL OTERO MAYORAL'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-28', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JESUS MIGUEL OTERO MAYORAL'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-29', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JESUS MIGUEL OTERO MAYORAL'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-30', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JESUS MIGUEL OTERO MAYORAL'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-31', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JESUS MIGUEL OTERO MAYORAL'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-06-22', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JOAQUIN ROMERO CARROZA'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-06-23', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JOAQUIN ROMERO CARROZA'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-06-24', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JOAQUIN ROMERO CARROZA'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-06-25', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JOAQUIN ROMERO CARROZA'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-06-26', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JOAQUIN ROMERO CARROZA'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-09-21', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JOAQUIN ROMERO CARROZA'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-09-22', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JOAQUIN ROMERO CARROZA'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-09-23', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JOAQUIN ROMERO CARROZA'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-09-24', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JOAQUIN ROMERO CARROZA'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-09-25', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JOAQUIN ROMERO CARROZA'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-03-11', 'ANJ', 'Sale al médico de 12 a 13 h', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JUAN ANTONIO DIAZ GONZALEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-05-27', 'BM', 'Pruebas médicas de 9 a 12h', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JUAN ANTONIO DIAZ GONZALEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-06-10', 'BM', 'Se va a las 10 por operación de un bulto en el brazo', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JUAN ANTONIO DIAZ GONZALEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-06-15', 'BM', 'Oculista de 8:30 a 11', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JUAN ANTONIO DIAZ GONZALEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-06-17', 'BM', 'Sale de 11:30 a 12:30 al hospital. Revisión operación bulto', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JUAN ANTONIO DIAZ GONZALEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-06-19', 'BM', 'Médico de cabecera a las 12:30', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JUAN ANTONIO DIAZ GONZALEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-02', 'OT', 'Sale de 11 a 13 por entrevista ingreso de su madre en una residencia', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JUAN ANTONIO DIAZ GONZALEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-16', 'BM', 'Médico de 10:30 a 12', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JUAN ANTONIO DIAZ GONZALEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-20', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JUAN ANTONIO DIAZ GONZALEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-21', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JUAN ANTONIO DIAZ GONZALEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-22', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JUAN ANTONIO DIAZ GONZALEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-23', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JUAN ANTONIO DIAZ GONZALEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-24', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JUAN ANTONIO DIAZ GONZALEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-27', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JUAN ANTONIO DIAZ GONZALEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-28', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JUAN ANTONIO DIAZ GONZALEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-29', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JUAN ANTONIO DIAZ GONZALEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-30', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JUAN ANTONIO DIAZ GONZALEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-31', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JUAN ANTONIO DIAZ GONZALEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-27', 'BM', 'Sale a las 12:30 una hora. Revisión oculista', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JUAN ANTONIO DIAZ GONZALEZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-02-03', 'OT', 'Pide trabajar solo hasta las 15:00 por psicólogo en la tarde', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JUAN JOSE MANCERA SANTOS'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-04-17', 'ANJ', 'Pide el día por operación de su mujer. No están casados y no le correspondería', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JUAN JOSE MANCERA SANTOS'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-05-08', 'ANJ', 'Pide el día por entierro de su tío', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JUAN JOSE MANCERA SANTOS'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-06-29', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JUAN JOSE MANCERA SANTOS'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-06-30', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JUAN JOSE MANCERA SANTOS'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-01', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JUAN JOSE MANCERA SANTOS'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-02', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JUAN JOSE MANCERA SANTOS'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-03', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JUAN JOSE MANCERA SANTOS'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-06', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JUAN JOSE MANCERA SANTOS'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-07', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JUAN JOSE MANCERA SANTOS'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-08', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JUAN JOSE MANCERA SANTOS'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-09', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JUAN JOSE MANCERA SANTOS'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-10', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JUAN JOSE MANCERA SANTOS'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-24', 'ANJ', 'Entra a las 10. Tenía que ir al banco', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JUAN JOSE MANCERA SANTOS'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-17', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JUAN LUIS HERNANDEZ CASTILLO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-17', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JUAN LUIS HERNANDEZ CASTILLO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-18', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JUAN LUIS HERNANDEZ CASTILLO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-19', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JUAN LUIS HERNANDEZ CASTILLO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-20', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JUAN LUIS HERNANDEZ CASTILLO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-21', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JUAN LUIS HERNANDEZ CASTILLO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-24', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JUAN LUIS HERNANDEZ CASTILLO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-25', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JUAN LUIS HERNANDEZ CASTILLO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-26', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JUAN LUIS HERNANDEZ CASTILLO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-27', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JUAN LUIS HERNANDEZ CASTILLO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-28', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JUAN LUIS HERNANDEZ CASTILLO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-02-09', 'AJ', 'Sale al médico a las 9:00 y no vuelve', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JUAN RAMON ALVAREZ ROBLES'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-02-26', 'AJ', 'Falta por pruebas médicas', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JUAN RAMON ALVAREZ ROBLES'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-03', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JUAN RAMON ALVAREZ ROBLES'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-04', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JUAN RAMON ALVAREZ ROBLES'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-05', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JUAN RAMON ALVAREZ ROBLES'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-06', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JUAN RAMON ALVAREZ ROBLES'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-07', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JUAN RAMON ALVAREZ ROBLES'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-10', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JUAN RAMON ALVAREZ ROBLES'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-11', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JUAN RAMON ALVAREZ ROBLES'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-12', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JUAN RAMON ALVAREZ ROBLES'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-13', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JUAN RAMON ALVAREZ ROBLES'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-14', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'JUAN RAMON ALVAREZ ROBLES'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-06-29', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'LUCAS HEREDIA SILVA'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-06-30', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'LUCAS HEREDIA SILVA'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-01', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'LUCAS HEREDIA SILVA'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-02', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'LUCAS HEREDIA SILVA'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-03', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'LUCAS HEREDIA SILVA'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-06', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'LUCAS HEREDIA SILVA'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-07', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'LUCAS HEREDIA SILVA'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-08', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'LUCAS HEREDIA SILVA'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-09', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'LUCAS HEREDIA SILVA'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-10', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'LUCAS HEREDIA SILVA'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-09-07', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'MARTA GALLEGO GUERRERO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-09-08', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'MARTA GALLEGO GUERRERO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-09-09', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'MARTA GALLEGO GUERRERO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-09-10', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'MARTA GALLEGO GUERRERO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-09-11', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'MARTA GALLEGO GUERRERO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-24', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'PEDRO ANTONIO DIAZ MUÑOZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-25', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'PEDRO ANTONIO DIAZ MUÑOZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-26', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'PEDRO ANTONIO DIAZ MUÑOZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-27', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'PEDRO ANTONIO DIAZ MUÑOZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-28', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'PEDRO ANTONIO DIAZ MUÑOZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-31', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'PEDRO ANTONIO DIAZ MUÑOZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-09-01', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'PEDRO ANTONIO DIAZ MUÑOZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-09-02', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'PEDRO ANTONIO DIAZ MUÑOZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-09-03', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'PEDRO ANTONIO DIAZ MUÑOZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-09-04', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'PEDRO ANTONIO DIAZ MUÑOZ'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-04-06', 'V', 'Feria de su pueblo', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'PEDRO CARROZA FLORES'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-06-11', 'AJ', 'Operación de su hija', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'PEDRO CARROZA FLORES'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-06-12', 'AJ', 'Postoperatorio de su hija', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'PEDRO CARROZA FLORES'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-24', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'PEDRO CARROZA FLORES'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-25', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'PEDRO CARROZA FLORES'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-26', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'PEDRO CARROZA FLORES'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-27', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'PEDRO CARROZA FLORES'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-28', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'PEDRO CARROZA FLORES'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-31', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'PEDRO CARROZA FLORES'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-09-01', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'PEDRO CARROZA FLORES'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-09-02', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'PEDRO CARROZA FLORES'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-09-03', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'PEDRO CARROZA FLORES'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-09-04', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'PEDRO CARROZA FLORES'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-09-07', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'RAMON ALVAREZ RAMOS'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-24', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'ROCIO RODRIGUEZ RIVAS'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-25', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'ROCIO RODRIGUEZ RIVAS'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-26', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'ROCIO RODRIGUEZ RIVAS'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-27', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'ROCIO RODRIGUEZ RIVAS'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-28', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'ROCIO RODRIGUEZ RIVAS'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-09-14', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'ROCIO RODRIGUEZ RIVAS'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-09-15', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'ROCIO RODRIGUEZ RIVAS'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-09-16', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'ROCIO RODRIGUEZ RIVAS'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-09-17', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'ROCIO RODRIGUEZ RIVAS'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-09-18', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'ROCIO RODRIGUEZ RIVAS'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-04-24', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'SERGIO DURAN PACHON'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-04-27', 'V', 'Pide los dos días premio de  Jerez motos', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'SERGIO DURAN PACHON'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-10', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'SERGIO DURAN PACHON'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-11', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'SERGIO DURAN PACHON'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-12', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'SERGIO DURAN PACHON'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-13', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'SERGIO DURAN PACHON'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-14', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'SERGIO DURAN PACHON'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-17', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'SERGIO DURAN PACHON'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-18', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'SERGIO DURAN PACHON'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-19', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'SERGIO DURAN PACHON'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-20', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'SERGIO DURAN PACHON'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-08-21', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'SERGIO DURAN PACHON'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-03-31', 'AJ', 'Se va a las 6 por fallecimiento de su padre', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'VICTOR BEJARANO OSORIO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-04-01', 'AJ', 'Entierro de su padre', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'VICTOR BEJARANO OSORIO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-06-05', 'OT', 'Pide salir 1 hora antes por un viaje', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'VICTOR BEJARANO OSORIO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-06', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'VICTOR BEJARANO OSORIO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-07', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'VICTOR BEJARANO OSORIO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-08', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'VICTOR BEJARANO OSORIO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-09', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'VICTOR BEJARANO OSORIO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-10', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'VICTOR BEJARANO OSORIO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-13', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'VICTOR BEJARANO OSORIO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-14', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'VICTOR BEJARANO OSORIO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-15', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'VICTOR BEJARANO OSORIO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-16', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'VICTOR BEJARANO OSORIO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

INSERT INTO vacaciones_ausencia
  (empleado_id, fecha, codigo, nota, adjunto, adjunto_nombre, usuario, fecha_registro)
SELECT e.id, '2026-07-17', 'V', '', '', '', 'import', datetime('now')
FROM vacaciones_empleado e
WHERE e.sede = 'merida' AND e.nombre = 'VICTOR BEJARANO OSORIO'
ON CONFLICT(empleado_id, fecha) DO UPDATE SET
  codigo = excluded.codigo,
  nota = excluded.nota,
  usuario = excluded.usuario,
  fecha_registro = excluded.fecha_registro;

-- Empleados de la lista no encontrados en plantilla Merida:
SELECT 'FALTA EMPLEADO: ' || x.nombre AS aviso FROM (
  SELECT 'ALEJANDRO ESPINO JIMENEZ' AS nombre
  UNION ALL SELECT 'ALFREDO ISMAEL CENTENO RICO'
  UNION ALL SELECT 'ALONSO MORENO GOMEZ'
  UNION ALL SELECT 'BLANCA GARCIA RUBIO'
  UNION ALL SELECT 'CARMEN MARIA TRINIDAD RAMOS'
  UNION ALL SELECT 'DAVID JIMENEZ CALERO'
  UNION ALL SELECT 'DAVID SANCHEZ SANCHEZ'
  UNION ALL SELECT 'DIEGO JOSE DELGADO ALVAREZ'
  UNION ALL SELECT 'FATIMA BONILLA GONZALEZ'
  UNION ALL SELECT 'GABRIEL BONILLA BENITEZ'
  UNION ALL SELECT 'IVAN CASTRO MERINO'
  UNION ALL SELECT 'JESUS MIGUEL OTERO MAYORAL'
  UNION ALL SELECT 'JOAQUIN ROMERO CARROZA'
  UNION ALL SELECT 'JUAN ANTONIO DIAZ GONZALEZ'
  UNION ALL SELECT 'JUAN JOSE MANCERA SANTOS'
  UNION ALL SELECT 'JUAN LUIS HERNANDEZ CASTILLO'
  UNION ALL SELECT 'JUAN RAMON ALVAREZ ROBLES'
  UNION ALL SELECT 'LUCAS HEREDIA SILVA'
  UNION ALL SELECT 'MARTA GALLEGO GUERRERO'
  UNION ALL SELECT 'PEDRO ANTONIO DIAZ MUÑOZ'
  UNION ALL SELECT 'PEDRO CARROZA FLORES'
  UNION ALL SELECT 'RAMON ALVAREZ RAMOS'
  UNION ALL SELECT 'ROCIO RODRIGUEZ RIVAS'
  UNION ALL SELECT 'SERGIO DURAN PACHON'
  UNION ALL SELECT 'VICTOR BEJARANO OSORIO'
) x WHERE NOT EXISTS (SELECT 1 FROM vacaciones_empleado e WHERE e.sede='merida' AND e.nombre=x.nombre);

COMMIT;
-- Total filas: 279
