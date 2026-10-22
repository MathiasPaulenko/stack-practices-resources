-- URL shortener: PostgreSQL schema for the write path (OLTP, low volume).
-- Reads hit Redis first; this table only sees cache misses and writes.

CREATE TABLE url_mappings (
    short_code VARCHAR(7) PRIMARY KEY,
    long_url   TEXT NOT NULL,
    user_id    BIGINT,
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    expires_at TIMESTAMP
);

-- Look up the original owner / stats page by long URL (dedupe checks).
CREATE INDEX idx_url_mappings_long_url ON url_mappings (long_url);

-- Purge job support: find expired links without a sequential scan.
CREATE INDEX idx_url_mappings_expires_at ON url_mappings (expires_at)
    WHERE expires_at IS NOT NULL;
