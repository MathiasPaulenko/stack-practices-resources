-- INCLUDE extra columns to enable Index Only Scans
CREATE INDEX idx_orders_covering
ON orders (customer_id, created_at DESC)
INCLUDE (total_amount, status);

-- This query can now be served entirely from the index
EXPLAIN (ANALYZE, BUFFERS)
SELECT customer_id, created_at, total_amount, status
FROM orders
WHERE customer_id = 1234
ORDER BY created_at DESC
LIMIT 50;

-- After heavy writes, keep Index Only Scans with a fresh visibility map
VACUUM ANALYZE orders;
