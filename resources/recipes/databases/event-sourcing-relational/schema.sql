-- Event sourcing schema for PostgreSQL
-- Run this to create the events and snapshots tables.

CREATE TABLE IF NOT EXISTS events (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    aggregate_id UUID NOT NULL,
    event_type   VARCHAR(255) NOT NULL,
    payload      JSONB NOT NULL,
    version      INTEGER NOT NULL,
    occurred_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_events_aggregate ON events (aggregate_id, version);
CREATE INDEX idx_events_type ON events (event_type);

CREATE TABLE IF NOT EXISTS snapshots (
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    aggregate_id UUID NOT NULL,
    version       INTEGER NOT NULL,
    state         JSONB NOT NULL,
    created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_snapshots_aggregate ON snapshots (aggregate_id, version DESC);

-- MySQL variant (uncomment to use):
-- CREATE TABLE IF NOT EXISTS events (
--     id          CHAR(36) PRIMARY KEY,
--     aggregate_id CHAR(36) NOT NULL,
--     event_type   VARCHAR(255) NOT NULL,
--     payload      JSON NOT NULL,
--     version      INT NOT NULL,
--     occurred_at  DATETIME NOT NULL DEFAULT NOW(),
--     INDEX idx_events_aggregate (aggregate_id, version)
-- );
--
-- CREATE TABLE IF NOT EXISTS snapshots (
--     id           CHAR(36) PRIMARY KEY,
--     aggregate_id CHAR(36) NOT NULL,
--     version       INT NOT NULL,
--     state         JSON NOT NULL,
--     created_at    DATETIME NOT NULL DEFAULT NOW(),
--     INDEX idx_snapshots_aggregate (aggregate_id, version DESC)
-- );
