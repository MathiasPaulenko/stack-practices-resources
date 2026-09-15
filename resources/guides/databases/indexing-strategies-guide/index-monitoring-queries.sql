-- Index Monitoring Queries
-- Track index usage, bloat, and effectiveness in production.

-- PostgreSQL: index usage stats (which indexes are being used)
SELECT schemaname,
       tablename,
       indexname,
       idx_scan AS scans,
       idx_tup_read AS tuples_read,
       idx_tup_fetch AS tuples_fetched,
       pg_size_pretty(pg_relation_size(indexrelid)) AS size
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;

-- PostgreSQL: index hit ratio (cache effectiveness)
-- A ratio below 90% means the index doesn't fit in shared_buffers.
SELECT schemaname,
       tablename,
       indexname,
       idx_blks_read,
       idx_blks_hit,
       round(100.0 * idx_blks_hit / NULLIF(idx_blks_read + idx_blks_hit, 0), 2) AS hit_ratio_pct
FROM pg_statio_user_indexes
ORDER BY hit_ratio_pct ASC NULLS LAST;

-- PostgreSQL: check index bloat (requires pgstattuple extension)
-- CREATE EXTENSION IF NOT EXISTS pgstattuple;
SELECT schemaname,
       tablename,
       indexname,
       pg_size_pretty(pg_relation_size(indexrelid)) AS size,
       avg_leaf_density,
       pg_size_pretty(pgstattuple(indexrelid).dead_tuple_len) AS dead_tuple_size
FROM pg_stat_user_indexes
JOIN pg_index ON indexrelid = pg_index.indexrelid
WHERE idx_scan > 0
ORDER BY pg_relation_size(indexrelid) DESC
LIMIT 20;

-- PostgreSQL: long-running index builds (check before starting CONCURRENTLY)
SELECT pid,
       age(now(), xact_start) AS transaction_duration,
       state,
       query
FROM pg_stat_activity
WHERE state = 'active'
  AND query NOT ILIKE '%pg_stat_activity%'
ORDER BY transaction_duration DESC;

-- MySQL: index usage via performance_schema
SELECT object_schema,
       object_name AS table_name,
       index_name,
       count_read,
       count_write,
       count_fetch,
       count_insert,
       count_update,
       count_delete
FROM performance_schema.table_io_waits_summary_by_index_usage
WHERE index_name IS NOT NULL
  AND object_schema NOT IN ('mysql', 'performance_schema', 'information_schema')
ORDER BY count_read DESC;

-- MySQL: index statistics (cardinality and size)
SELECT table_schema,
       table_name,
       index_name,
       non_unique,
       seq_in_index,
       cardinality,
       index_type
FROM information_schema.statistics
WHERE table_schema NOT IN ('mysql', 'information_schema', 'performance_schema')
ORDER BY table_schema, table_name, index_name, seq_in_index;
