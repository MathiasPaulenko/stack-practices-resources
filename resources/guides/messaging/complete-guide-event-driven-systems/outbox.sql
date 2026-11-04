-- Transactional outbox table (Postgres)
CREATE TABLE outbox (
    event_id      UUID PRIMARY KEY,
    aggregate_id  VARCHAR(255) NOT NULL,
    aggregate_type VARCHAR(100) NOT NULL,
    event_type    VARCHAR(100) NOT NULL,
    data          JSONB NOT NULL,
    created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    published     BOOLEAN NOT NULL DEFAULT FALSE,
    published_at  TIMESTAMPTZ
);

CREATE INDEX idx_outbox_unpublished ON outbox (created_at)
    WHERE published = FALSE;

-- Relay pattern: poll with FOR UPDATE SKIP LOCKED, publish, mark published.
-- Cleanup: DELETE FROM outbox WHERE published AND published_at < NOW() - INTERVAL '7 days';
