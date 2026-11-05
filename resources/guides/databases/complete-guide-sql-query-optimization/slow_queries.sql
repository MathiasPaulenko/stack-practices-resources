-- Finding slow queries.
-- PostgreSQL: pg_stat_statements + pg_stat_activity
-- MySQL: slow query log + Performance Schema

-- ============================ PostgreSQL ============================
-- One-time setup: add pg_stat_statements to shared_preload_libraries in
-- postgresql.conf, restart, then:

CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- Top 10 queries by TOTAL time — optimize these first.
SELECT query, calls, total_exec_time, mean_exec_time, rows
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 10;

-- Same ranking by mean time, for queries you already know are hot.
SELECT query, calls, mean_exec_time, rows
FROM pg_stat_statements
WHERE calls > 100
ORDER BY mean_exec_time DESC
LIMIT 10;

-- What is slow RIGHT NOW (queries holding locks / blocking others).
SELECT pid, now() - query_start AS duration, state, query
FROM pg_stat_activity
WHERE state = 'active'
  AND now() - query_start > interval '1 second'
  AND query NOT LIKE '%pg_stat_activity%'
ORDER BY duration DESC;

-- Index usage audit: idx_scan = 0 means drop candidates
-- (verify the index does not back a UNIQUE/FK constraint first).
SELECT schemaname, relname, indexrelname, idx_scan, idx_tup_read
FROM pg_stat_user_indexes
ORDER BY idx_scan ASC, relname;

-- Buffer cache hit ratio per table (low = cache misses).
SELECT relname, heap_blks_read, heap_blks_hit,
       ROUND(100.0 * heap_blks_hit /
             NULLIF(heap_blks_read + heap_blks_hit, 0), 1) AS hit_pct
FROM pg_statio_user_tables
ORDER BY hit_pct ASC NULLS LAST;

-- =============================== MySQL ==============================
-- Enable the slow log at runtime (persist in my.cnf):
--   slow_query_log = 1
--   long_query_time = 1
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 1;

-- Top normalized statements by total time.
SELECT DIGEST_TEXT, COUNT_STAR,
       SUM_TIMER_WAIT / 1e12 AS total_sec,
       AVG_TIMER_WAIT / 1e12 AS avg_sec
FROM performance_schema.events_statements_summary_by_digest
ORDER BY SUM_TIMER_WAIT DESC
LIMIT 10;

-- Statements doing full table scans.
SELECT DIGEST_TEXT, COUNT_STAR, SUM_NO_INDEX_USED
FROM performance_schema.events_statements_summary_by_digest
WHERE SUM_NO_INDEX_USED > 0
ORDER BY SUM_NO_INDEX_USED DESC
LIMIT 10;
