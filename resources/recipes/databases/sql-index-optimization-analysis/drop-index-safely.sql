-- 1) Monitor usage for at least a week first (see find-unused-indexes.sql)
-- 2) Check the index size before dropping
SELECT pg_size_pretty(pg_relation_size('idx_orders_old_status'));

-- 3) Drop without locking the table
DROP INDEX CONCURRENTLY idx_orders_old_status;
