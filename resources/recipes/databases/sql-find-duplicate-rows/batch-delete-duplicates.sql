-- Batch deletion for large tables (PostgreSQL)
-- Deletes duplicates in chunks of 1000 with a short sleep between batches
-- to avoid long transactions and lock contention.
-- Source: https://stackpractices.com/recipes/sql-find-duplicate-rows/

DO $$
DECLARE
  deleted_count INTEGER;
BEGIN
  LOOP
    WITH duplicates AS (
      SELECT id,
             ROW_NUMBER() OVER (PARTITION BY email ORDER BY created_at) AS rn
      FROM users
      LIMIT 5000
    )
    DELETE FROM users
    WHERE id IN (SELECT id FROM duplicates WHERE rn > 1 LIMIT 1000);

    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    EXIT WHEN deleted_count = 0;

    RAISE NOTICE 'Deleted % rows', deleted_count;
    PERFORM pg_sleep(0.1);  -- throttle between batches
  END LOOP;
END $$;

-- After a large deduplication, refresh planner statistics and reclaim space:
ANALYZE users;
-- For severe index bloat, run during a maintenance window:
-- REINDEX INDEX idx_users_email;
-- VACUUM FULL users;  -- exclusive lock, maintenance window only
