-- CosmoStore (M7–M8) - PostgreSQL setup
-- Ajusta la contraseña según tu .env (DB_PASSWORD)

CREATE DATABASE ecommerce_db;

CREATE USER ecommerce_user WITH PASSWORD 'TU_PASSWORD_AQUI';

GRANT ALL PRIVILEGES ON DATABASE ecommerce_db TO ecommerce_user;

-- Opcional: si quieres que el usuario pueda crear/alterar objetos sin problemas
ALTER DATABASE ecommerce_db OWNER TO ecommerce_user;
