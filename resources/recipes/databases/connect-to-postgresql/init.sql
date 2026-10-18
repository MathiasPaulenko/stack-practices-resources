CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    active BOOLEAN NOT NULL DEFAULT TRUE
);

INSERT INTO users (email) VALUES
    ('alice@example.com'),
    ('bob@example.com'),
    ('carol@example.com')
ON CONFLICT (email) DO NOTHING;

CREATE TABLE IF NOT EXISTS accounts (
    id SERIAL PRIMARY KEY,
    balance NUMERIC(12, 2) NOT NULL DEFAULT 0
);

INSERT INTO accounts (balance) VALUES (100.00), (50.00);
