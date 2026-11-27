-- Guardrails: fail fast instead of blocking the database
SET statement_timeout = '30s';
SET lock_timeout = '5s';
ALTER TABLE customers ADD COLUMN email_address VARCHAR(255);
SET statement_timeout = '0';
SET lock_timeout = '0';

-- Watch for lock waits during the migration
SELECT pid, state, wait_event_type, wait_event,
       now() - query_start AS duration, query
FROM pg_stat_activity
WHERE state != 'idle'
ORDER BY duration DESC;
