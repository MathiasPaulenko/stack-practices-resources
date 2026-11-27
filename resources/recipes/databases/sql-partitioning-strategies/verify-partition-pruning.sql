-- Confirm the planner skips irrelevant partitions
EXPLAIN ANALYZE
SELECT * FROM orders
WHERE created_at >= '2024-01-15' AND created_at < '2024-02-01';
-- Only orders_2024_01 should appear in the plan

-- Static pruning: literal known at plan time
SELECT * FROM orders WHERE created_at = '2024-01-15';

-- Dynamic pruning: prunes at execution time
PREPARE get_orders(DATE) AS
  SELECT * FROM orders WHERE created_at = $1;
EXECUTE get_orders('2024-01-15');

-- Make sure pruning is enabled (default on since PG11)
SHOW enable_partition_pruning;
