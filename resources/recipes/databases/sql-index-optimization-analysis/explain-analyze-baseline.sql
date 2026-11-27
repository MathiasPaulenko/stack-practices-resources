-- Baseline: analyze a slow query before adding an index
EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)
SELECT * FROM orders
WHERE customer_id = 1234
  AND created_at > '2024-01-01'
ORDER BY created_at DESC
LIMIT 100;

-- If the plan shows a Seq Scan, create a composite index
CREATE INDEX idx_orders_customer_created
ON orders (customer_id, created_at DESC);

-- Re-run the same EXPLAIN to measure the improvement
