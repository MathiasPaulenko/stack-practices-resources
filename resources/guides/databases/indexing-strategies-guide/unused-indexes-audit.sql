-- Unused Index Audit Script
-- Run quarterly to find indexes that are never used by the query planner.
-- Dropping unused indexes reduces write amplification and storage.

-- PostgreSQL: find unused indexes ordered by size (biggest waste first)
SELECT schemaname,
       tablename,
       indexname,
       pg_size_pretty(pg_relation_size(indexrelid)) AS index_size,
       idx_scan AS scan_count
FROM pg_stat_user_indexes
WHERE idx_scan = 0
  AND indexrelname NOT LIKE 'pg_toast%'
  AND indexrelname NOT LIKE '%_pkey'  -- skip primary keys
ORDER BY pg_relation_size(indexrelid) DESC;

-- PostgreSQL: find indexes with low usage (used but rarely)
SELECT schemaname,
       tablename,
       indexname,
       pg_size_pretty(pg_relation_size(indexrelid)) AS index_size,
       idx_scan AS scan_count,
       idx_tup_read,
       idx_tup_fetch
FROM pg_stat_user_indexes
WHERE idx_scan > 0 AND idx_scan < 10
ORDER BY pg_relation_size(indexrelid) DESC;

-- MySQL: find unused indexes via performance_schema
SELECT object_schema,
       object_name AS table_name,
       index_name,
       count_read,
       count_write
FROM performance_schema.table_io_waits_summary_by_index_usage
WHERE index_name IS NOT NULL
  AND count_read = 0
  AND object_schema NOT IN ('mysql', 'performance_schema', 'information_schema')
ORDER BY count_write DESC;

-- Action: DROP indexes with scan_count = 0 after confirming they're not
-- needed for constraints (UNIQUE, PRIMARY KEY) or future planned queries.
--
-- Example:
--   DROP INDEX CONCURRENTLY idx_users_inactive_email;
--
-- Always use CONCURRENTLY in production to avoid locking the table.
