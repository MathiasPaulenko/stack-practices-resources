-- Index only non-deleted rows: much smaller when most rows are deleted
CREATE INDEX idx_orders_active_customer
ON orders (customer_id)
WHERE deleted_at IS NULL;

-- The query must match the index predicate to use it
EXPLAIN ANALYZE
SELECT * FROM orders
WHERE customer_id = 1234 AND deleted_at IS NULL;
