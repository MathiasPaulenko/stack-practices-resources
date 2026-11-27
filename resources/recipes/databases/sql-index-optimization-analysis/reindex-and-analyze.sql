-- Check the largest indexes and their scan counts
SELECT schemaname, relname, indexrelname,
       pg_size_pretty(pg_relation_size(indexrelid)) AS size,
       idx_scan AS scans
FROM pg_stat_user_indexes
ORDER BY pg_relation_size(indexrelid) DESC
LIMIT 20;

-- Rebuild a bloated index without locking the table
REINDEX INDEX CONCURRENTLY idx_orders_customer_created;

-- Or rebuild every index on a table
REINDEX TABLE CONCURRENTLY orders;

-- Refresh planner statistics after bulk loads
ANALYZE orders;

-- Raise the statistics target for better estimates on skewed columns
ALTER TABLE orders ALTER COLUMN customer_id SET STATISTICS 1000;
ANALYZE orders;
