-- top-slow-queries.sql — find the queries worth optimizing, ranked by total time.
-- Companion to: https://stackpractices.com/docs/database-query-tuning-checklist/
-- PostgreSQL: requires pg_stat_statements (CREATE EXTENSION once per database).

-- ── Install once ──────────────────────────────────────────────
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- ── Top 20 queries by TOTAL execution time ────────────────────
-- Prioritize these: a 50ms query at 2,000 calls/min costs more
-- than a 5s query that runs nightly.
SELECT
  calls,
  round(mean_exec_time::numeric, 2)  AS mean_ms,
  round(max_exec_time::numeric, 2)   AS max_ms,
  round(total_exec_time::numeric, 0) AS total_ms,
  rows                               AS rows_returned,
  left(query, 120)                   AS query
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 20;

-- ── Queries with the worst cache hit ratio ────────────────────
-- shared_blks_read > hit means disk I/O — either working set is
-- bigger than shared_buffers, or the query scans more than it should.
SELECT
  calls,
  round(mean_exec_time::numeric, 2) AS mean_ms,
  shared_blks_read,
  shared_blks_hit,
  round(100.0 * shared_blks_hit / nullif(shared_blks_hit + shared_blks_read, 0), 1)
    AS cache_hit_pct,
  left(query, 100) AS query
FROM pg_stat_statements
WHERE shared_blks_read + shared_blks_hit > 0
ORDER BY shared_blks_read DESC
LIMIT 20;

-- ── Enable the slow log for the un-instrumented window ────────
-- ALTER SYSTEM SET log_min_duration_statement = 100;  -- 100ms+
-- SELECT pg_reload_conf();

-- ── MySQL equivalent ──────────────────────────────────────────
-- SELECT schema_name, exec_count, avg_timer_wait/1e9 AS avg_ms,
--        sum_timer_wait/1e9 AS total_ms, digest_text
-- FROM performance_schema.events_statements_summary_by_digest
-- ORDER BY sum_timer_wait DESC LIMIT 20;
