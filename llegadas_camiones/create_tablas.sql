-- Tablas Control horario llegada de camiones (SQLite)
-- sqlite3 /vehiculosagenda/vehiculosagenda/database/VEHICULOS.db < llegadas_camiones/create_tablas.sql

CREATE TABLE IF NOT EXISTS llegada_camion_dia (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  fecha DATE NOT NULL UNIQUE,
  turno VARCHAR(100) DEFAULT 'MÉRIDA LLEGADAS',
  usuario VARCHAR(100) DEFAULT '',
  fecha_registro DATETIME
);

CREATE TABLE IF NOT EXISTS llegada_camion_linea (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  dia_id INTEGER NOT NULL,
  orden INTEGER DEFAULT 0,
  agencia VARCHAR(120) DEFAULT '',
  ruta VARCHAR(200) DEFAULT '',
  matricula VARCHAR(50) DEFAULT '',
  hora_llegada VARCHAR(10) DEFAULT '',
  fin_descarga VARCHAR(10) DEFAULT '',
  pallets VARCHAR(50) DEFAULT '',
  personas VARCHAR(200) DEFAULT '',
  es_manual BOOLEAN DEFAULT 0,
  usuario_mod VARCHAR(100) DEFAULT '',
  fecha_mod DATETIME,
  FOREIGN KEY(dia_id) REFERENCES llegada_camion_dia(id)
);

CREATE INDEX IF NOT EXISTS ix_llegada_camion_linea_dia_orden
  ON llegada_camion_linea(dia_id, orden);
