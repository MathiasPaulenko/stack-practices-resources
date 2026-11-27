-- Weekly index health check. Run via cron and log the results.

-- 1. Top 10 largest indexes (review candidates)
SELECT relname, indexrelname,
       pg_size_pretty(pg_relation_size(indexrelid)) AS size
FROM pg_stat_user_indexes
ORDER BY pg_relation_size(indexrelid) DESC
LIMIT 10;

-- 2. Indexes with zero scans (unused)
SELECT relname, indexrelname, idx_scan
FROM pg_stat_user_indexes
WHERE idx_scan = 0
ORDER BY pg_relation_size(indexrelid) DESC;

-- 3. Tables under sequential scan pressure
SELECT relname, seq_scan, seq_tup_read, idx_scan, idx_tup_fetch
FROM pg_stat_user_tables
WHERE seq_scan > 100 AND seq_tup_read > idx_tup_fetch
ORDER BY seq_tup_read DESC;
