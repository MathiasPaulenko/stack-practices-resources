-- Session guards for migration runners (PostgreSQL)

SET lock_timeout = '5s';        -- fail fast instead of queueing behind a long txn
SET statement_timeout = '60s';  -- bound runaway DDL

-- Progress + health checks
-- Watch a CONCURRENTLY index build:
--   SELECT * FROM pg_stat_progress_create_index;
-- Watch replica lag during backfills:
SELECT now() - pg_last_xact_replay_timestamp() AS replication_lag;

-- Refresh planner statistics after large backfills
ANALYZE users;
