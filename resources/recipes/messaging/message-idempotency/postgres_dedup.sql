-- PostgreSQL deduplication table with a unique primary key.
CREATE TABLE IF NOT EXISTS processed_messages (
    message_id UUID PRIMARY KEY,
    processed_at TIMESTAMPTZ DEFAULT NOW(),
    result JSONB
);

-- Example transaction. Replace placeholders with your business logic.
-- The UPDATE only runs when the message_id was actually inserted.
BEGIN;

WITH inserted AS (
    INSERT INTO processed_messages (message_id, result)
    VALUES (
        'msg_abc123'::UUID,
        '{"status": "shipped"}'::JSONB
    )
    ON CONFLICT (message_id) DO NOTHING
    RETURNING message_id
)
UPDATE inventory
SET quantity = 10
WHERE id = 1
  AND EXISTS (SELECT 1 FROM inserted);

COMMIT;
