-- Reference schema for the ORM CRUD examples (PostgreSQL syntax).
-- The ORMs can generate this from their models; this file shows what they produce.

CREATE TABLE users (
    id    SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    role  VARCHAR(50) NOT NULL DEFAULT 'user'
);

CREATE INDEX idx_users_role ON users (role);

CREATE TABLE posts (
    id      SERIAL PRIMARY KEY,
    title   VARCHAR(255) NOT NULL,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_posts_user_id ON posts (user_id);
