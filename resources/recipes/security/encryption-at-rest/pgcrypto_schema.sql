-- PostgreSQL 16+ pgcrypto schema for searchable encryption.
-- Run: psql -d mydb -f pgcrypto_schema.sql

CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Schema for searchable encryption with blind index.
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email_encrypted TEXT NOT NULL,             -- AES-256-GCM ciphertext
    email_nonce TEXT NOT NULL,                 -- Nonce for decryption
    email_blind_index VARCHAR(64) NOT NULL,    -- HMAC for exact-match queries
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Create index on blind index for fast lookups.
CREATE INDEX IF NOT EXISTS idx_users_email_blind ON users(email_blind_index);

-- Encrypt before insert (using application-side encryption).
-- INSERT INTO users (email_encrypted, email_nonce, email_blind_index)
-- VALUES ('base64ciphertext', 'base64nonce', 'hmac_blind_index_value');

-- Query by email without decrypting all rows.
-- SELECT * FROM users
-- WHERE email_blind_index = generate_blind_index('user@example.com');

-- Alternatively, use pgcrypto directly for column-level encryption:
INSERT INTO users (email_encrypted, email_nonce, email_blind_index)
VALUES (
    pgp_sym_encrypt('user@example.com', current_setting('app.encryption_key'))::text,
    '',
    encode(hmac('user@example.com'::bytea, current_setting('app.index_key')::bytea, 'sha256'), 'hex')
);

-- Decrypt on select.
SELECT
    id,
    pgp_sym_decrypt(email_encrypted::bytea, current_setting('app.encryption_key')) as email
FROM users
WHERE email_blind_index = encode(hmac('user@example.com'::bytea, current_setting('app.index_key')::bytea, 'sha256'), 'hex');
