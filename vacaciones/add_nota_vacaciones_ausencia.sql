-- Añadir columna nota a vacaciones_ausencia (SQLite)
-- Si ya existe: error "duplicate column name: nota" → ignorar y seguir.
--
-- sqlite3 /ruta/database/VEHICULOS.db < vacaciones/add_nota_vacaciones_ausencia.sql

ALTER TABLE vacaciones_ausencia ADD COLUMN nota VARCHAR(1000) DEFAULT '';
