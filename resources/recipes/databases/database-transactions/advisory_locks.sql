-- PostgreSQL advisory locks: application-defined locks stored in the database.
-- They don't protect any table — they coordinate whoever bothers to check them.

-- Transaction-level: released automatically on commit or rollback
BEGIN;
SELECT pg_advisory_xact_lock(12345);
-- ... critical section ...
COMMIT;

-- Session-level: must be released explicitly
SELECT pg_advisory_lock(12345);
-- ... critical section ...
SELECT pg_advisory_unlock(12345);

-- Non-blocking: returns true/false right away
SELECT pg_try_advisory_lock(12345);

-- LISTEN/NOTIFY: lightweight cross-process events delivered at commit time
-- Process 1: subscribe to the channel
LISTEN order_created;

-- Process 2: fire inside or after a transaction
NOTIFY order_created, '{"order_id": 42, "customer": "alice"}';
