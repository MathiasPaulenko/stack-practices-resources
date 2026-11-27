-- Spot hot partitions or uneven distribution
SELECT tablename,
       pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE tablename LIKE 'orders_2024%'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Watch the default partition: it should stay small
SELECT pg_size_pretty(pg_total_relation_size('customers_default'));
