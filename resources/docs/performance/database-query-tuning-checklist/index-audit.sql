-- index-audit.sql — audit index health on PostgreSQL.
-- Companion to: https://stackpractices.com/docs/database-query-tuning-checklist/
-- Answers: what indexes exist, which are unused, which are missing
-- (tables doing heavy seq scans), and index selectivity candidates.

-- ── 1. All indexes + usage per table ──────────────────────────
SELECT
  schemaname,
  relname        AS table_name,
  indexrelname   AS index_name,
  idx_scan       AS times_used,
  pg_size_pretty(pg_relation_size(indexrelid)) AS index_size
FROM pg_stat_user_indexes
ORDER BY relname, idx_scan DESC;

-- ── 2. Unused indexes (dead weight on writes) ─────────────────
SELECT
  schemaname,
  relname,
  indexrelname,
  pg_size_pretty(pg_relation_size(indexrelid)) AS wasted_size
FROM pg_stat_user_indexes
WHERE idx_scan = 0
ORDER BY pg_relation_size(indexrelid) DESC;

-- ── 3. Tables with heavy sequential scans (missing index?) ────
-- seq_scan high relative to idx_scan + enough rows = candidate
SELECT
  relname,
  seq_scan,
  seq_tup_read,
  idx_scan,
  n_live_tup
FROM pg_stat_user_tables
WHERE seq_scan > 0
  AND n_live_tup > 1000
ORDER BY seq_tup_read DESC
LIMIT 20;

-- ── 4. Column selectivity (index candidacy) ───────────────────
-- Fill in table + column; > 0.3 selectivity = decent candidate
-- SELECT COUNT(DISTINCT <column>)::float / COUNT(*) AS selectivity
-- FROM <table>;

-- ── 5. Duplicate indexes (same columns, different order/name) ─
SELECT
  a.indrelid::regclass AS table_name,
  a.indexrelid::regclass AS index_a,
  b.indexrelid::regclass AS index_b
FROM pg_index a
JOIN pg_index b ON a.indrelid = b.indrelid
  AND a.indexrelid < b.indexrelid
  AND a.indkey = b.indkey;

-- ── MySQL equivalents ─────────────────────────────────────────
-- SHOW INDEX FROM orders;
-- SELECT * FROM sys.schema_unused_indexes;
-- SELECT * FROM sys.table_scan_waits_summary_by_table ORDER BY total_wait DESC;
