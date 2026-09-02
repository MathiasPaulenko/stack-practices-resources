#!/bin/sh
set -e

echo "Initializing database..."
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE TABLE IF NOT EXISTS app_data (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        created_at TIMESTAMP DEFAULT NOW()
    );
    INSERT INTO app_data (name) VALUES ('sample entry') ON CONFLICT DO NOTHING;
EOSQL

echo "Database initialized."
