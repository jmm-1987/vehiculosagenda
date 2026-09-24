-- Tabla Rectificaciones (SQLite)
-- sqlite3 /vehiculosagenda/vehiculosagenda/database/VEHICULOS.db < rectificaciones/create_tablas.sql

CREATE TABLE IF NOT EXISTS rectificacion (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  fecha DATE,
  expedicion VARCHAR(100) DEFAULT '',
  agencia VARCHAR(80) DEFAULT '',
  peso_documentado FLOAT,
  peso_real FLOAT,
  diferencia_peso FLOAT,
  vol_documentado FLOAT,
  vol_real FLOAT,
  diferencia_vol FLOAT,
  pvkg_documentado FLOAT,
  pvkg_real FLOAT,
  estado VARCHAR(20) DEFAULT 'Pendiente',
  usuario VARCHAR(100) DEFAULT '',
  fecha_registro DATETIME
);

CREATE INDEX IF NOT EXISTS ix_rectificacion_fecha ON rectificacion(fecha);
CREATE INDEX IF NOT EXISTS ix_rectificacion_agencia ON rectificacion(agencia);
