-- EXPLAIN ANALYZE exercises matching the query-optimization recipe.
-- Run schema.sql first.

-- Baseline: orders for one customer, unindexed customer_id -> Seq Scan.
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM orders WHERE customer_id = 42;

-- Add an index and compare the plan.
CREATE INDEX IF NOT EXISTS idx_orders_customer ON orders(customer_id);
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM orders WHERE customer_id = 42;

-- Covering index: the query reads only indexed columns -> Index Only Scan.
CREATE INDEX IF NOT EXISTS idx_orders_customer_total
    ON orders(customer_id) INCLUDE (total, status);
EXPLAIN (ANALYZE, BUFFERS)
SELECT customer_id, total, status FROM orders WHERE customer_id = 42;

-- N+1 in SQL form: a correlated subquery per row.
EXPLAIN (ANALYZE, BUFFERS)
SELECT o.id,
       (SELECT name FROM customers c WHERE c.id = o.customer_id) AS customer_name
FROM orders o
LIMIT 100;

-- Same result, one join.
EXPLAIN (ANALYZE, BUFFERS)
SELECT o.id, c.name AS customer_name
FROM orders o
JOIN customers c ON c.id = o.customer_id
LIMIT 100;

-- OFFSET pagination gets slower with depth.
EXPLAIN (ANALYZE, BUFFERS)
SELECT id, created_at FROM orders ORDER BY created_at DESC LIMIT 20 OFFSET 100000;

-- Keyset pagination stays flat at any depth.
CREATE INDEX IF NOT EXISTS idx_orders_created ON orders(created_at DESC);
EXPLAIN (ANALYZE, BUFFERS)
SELECT id, created_at FROM orders
WHERE created_at < now() - interval '200 days'
ORDER BY created_at DESC
LIMIT 20;

-- NOT IN vs NOT EXISTS.
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM customers c
WHERE c.id NOT IN (SELECT customer_id FROM orders);

EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM customers c
WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id);
