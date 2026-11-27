-- Test whether an index would be used before creating it
CREATE EXTENSION IF NOT EXISTS hypopg;

-- Register a hypothetical index
SELECT * FROM hypopg_create_index('orders', 'customer_id, created_at');

-- Check the plan the planner would choose
EXPLAIN SELECT * FROM orders WHERE customer_id = 1234 AND created_at > '2024-01-01';

-- Clean up
SELECT hypopg_reset();
