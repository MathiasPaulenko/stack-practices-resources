-- Monitoring queries from the query-optimization recipe.

-- 1. Enable slow query logging (postgresql.conf or ALTER SYSTEM).
--    ALTER SYSTEM SET log_min_duration_statement = '1000ms';
--    SELECT pg_reload_conf();

-- 2. pg_stat_statements setup (run once as superuser).
--    CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- Top 10 most expensive queries by total time.
SELECT query,
       calls,
       mean_exec_time,
       total_exec_time,
       rows
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 10;

-- Unstable queries: high variance usually means parameter-sensitive plans.
SELECT query,
       calls,
       mean_exec_time,
       stddev_exec_time
FROM pg_stat_statements
WHERE calls > 10
ORDER BY stddev_exec_time DESC
LIMIT 10;

-- Reset statistics after deploying a fix for a clean before/after.
-- SELECT pg_stat_statements_reset();
