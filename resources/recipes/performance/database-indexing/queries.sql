-- Demo queries paired with the indexes in indexes.sql.
-- Run EXPLAIN (ANALYZE, BUFFERS) on each to see index usage.

-- 1. Single-column index → Index Scan
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'alice@example.com';

-- 2. Composite index → Index Scan on leftmost prefix
EXPLAIN ANALYZE SELECT * FROM orders WHERE user_id = 42;

-- 3. Composite index → Index Scan + no sort step
EXPLAIN ANALYZE
SELECT * FROM orders WHERE user_id = 42
ORDER BY created_at DESC LIMIT 10;

-- 4. Partial index → only used when the predicate matches
EXPLAIN ANALYZE SELECT * FROM orders WHERE user_id = 42 AND deleted_at IS NULL;

-- 5. Covering index → Index Only Scan (Heap Fetches: 0)
EXPLAIN ANALYZE
SELECT total_amount, created_at FROM orders
WHERE user_id = 42 AND status = 'paid';

-- 6. Expression index → used when the expression matches exactly
EXPLAIN ANALYZE SELECT * FROM users WHERE LOWER(email) = 'alice@example.com';

-- 7. Keyset pagination → no OFFSET, constant time per page
EXPLAIN ANALYZE
SELECT * FROM orders
WHERE (created_at, id) < ('2025-01-15', 12345)
ORDER BY created_at DESC, id DESC LIMIT 20;

-- 8. FK index → deleting a parent row stays fast
EXPLAIN ANALYZE DELETE FROM users WHERE id = 1;

-- Maintenance queries (PostgreSQL):

-- Unused indexes (idx_scan = 0)
SELECT schemaname, indexname, idx_scan
FROM pg_stat_user_indexes
WHERE idx_scan = 0 ORDER BY indexname;

-- Foreign keys without a supporting index
SELECT conrelid::regclass AS table_name, conname AS constraint_name
FROM pg_constraint WHERE contype = 'f'
AND NOT EXISTS (
  SELECT 1 FROM pg_index WHERE indrelid = conrelid AND conkey @> indkey
);

-- HOT update ratio per table
SELECT relname, n_tup_hot_upd::float / NULLIF(n_tup_upd, 0) AS hot_ratio
FROM pg_stat_user_tables WHERE n_tup_upd > 0;
