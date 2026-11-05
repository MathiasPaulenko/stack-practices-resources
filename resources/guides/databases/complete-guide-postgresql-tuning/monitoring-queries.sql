-- Monitoring queries from the PostgreSQL tuning guide.

-- Top queries by total execution time (needs pg_stat_statements)
SELECT
  calls,
  ROUND(total_exec_time::numeric, 0) AS total_ms,
  ROUND(mean_exec_time::numeric, 2) AS mean_ms,
  LEFT(query, 80) AS query
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 20;

-- Table bloat: dead tuples as % of live rows
SELECT
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname || '.' || tablename)) AS size,
    n_live_tup,
    n_dead_tup,
    ROUND(n_dead_tup::FLOAT / NULLIF(n_live_tup, 0) * 100, 2) AS dead_pct
FROM pg_stat_user_tables
ORDER BY n_dead_tup DESC
LIMIT 20;

-- What's running right now
SELECT pid, now() - query_start AS duration, query, state
FROM pg_stat_activity
WHERE state != 'idle'
ORDER BY duration DESC;

-- Index usage — near-zero scans are removal candidates
SELECT
    schemaname,
    tablename,
    indexname,
    idx_scan AS scans
FROM pg_stat_user_indexes
ORDER BY idx_scan ASC
LIMIT 20;

-- Cache hit ratio per table (aim >95%)
SELECT
    relname,
    ROUND(heap_blks_hit::FLOAT / NULLIF(heap_blks_hit + heap_blks_read, 0) * 100, 2) AS hit_ratio
FROM pg_statio_user_tables
ORDER BY hit_ratio ASC
LIMIT 20;

-- Database-level cache hit ratio
SELECT
    datname,
    ROUND(blks_hit::FLOAT / NULLIF(blks_hit + blks_read, 0) * 100, 2) AS cache_hit_ratio
FROM pg_stat_database;

-- Autovacuum progress
SELECT pid, phase, heap_blks_total, heap_blks_scanned
FROM pg_stat_progress_vacuum;

-- Unused indexes (check pg_stat_reset timing before dropping!)
SELECT schemaname, tablename, indexname, idx_scan
FROM pg_stat_user_indexes
WHERE idx_scan = 0
ORDER BY pg_total_relation_size(schemaname || '.' || indexname) DESC;
