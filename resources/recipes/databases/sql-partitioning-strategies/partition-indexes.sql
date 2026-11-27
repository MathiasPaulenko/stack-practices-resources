-- Indexes on the parent propagate to every partition
CREATE INDEX idx_orders_customer ON orders (customer_id);

-- Include the partition key when the query filters on both
CREATE INDEX idx_orders_customer_date ON orders (customer_id, created_at);

-- Verify child partitions got their local indexes
SELECT tablename, indexname FROM pg_indexes
WHERE tablename LIKE 'orders_2024%'
ORDER BY tablename, indexname;
