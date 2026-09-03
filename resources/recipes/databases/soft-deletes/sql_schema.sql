-- Schema for soft deletes examples.
-- Supports: PostgreSQL, SQLite (with minor syntax changes).

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    deleted_at TIMESTAMP NULL,
    deleted_by VARCHAR(100)
);

CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    title VARCHAR(255) NOT NULL,
    body TEXT,
    deleted_at TIMESTAMP NULL,
    deleted_by VARCHAR(100)
);

-- Partial unique index: only one active user per email.
-- Multiple soft-deleted rows with the same email are allowed.
CREATE UNIQUE INDEX idx_users_email_active
ON users (email)
WHERE deleted_at IS NULL;

-- Partial index for active queries (keeps index small).
CREATE INDEX idx_posts_active_user
ON posts (user_id)
WHERE deleted_at IS NULL;

-- Audit table for hard delete logging.
CREATE TABLE soft_delete_audit (
    id SERIAL PRIMARY KEY,
    table_name VARCHAR(100) NOT NULL,
    record_id INTEGER NOT NULL,
    action VARCHAR(20) NOT NULL,
    deleted_by VARCHAR(100),
    deleted_at TIMESTAMP NOT NULL DEFAULT NOW()
);
