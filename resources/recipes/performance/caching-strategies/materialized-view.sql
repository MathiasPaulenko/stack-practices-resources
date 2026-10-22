-- PostgreSQL: buffer pool tuning + a materialized view for expensive aggregations.
-- Apply the settings in postgresql.conf, then reload: SELECT pg_reload_conf();

-- postgresql.conf
-- shared_buffers = 4GB                  -- ~25% of RAM
-- effective_cache_size = 12GB           -- OS + PostgreSQL cache total
-- work_mem = 256MB                      -- per-query sort/hash memory

CREATE MATERIALIZED VIEW daily_sales_summary AS
SELECT
    date_trunc('day', created_at) AS day,
    sum(amount) AS total_sales,
    count(*) AS order_count
FROM orders
WHERE created_at > now() - interval '90 days'
GROUP BY 1;

-- Unique index enables CONCURRENTLY refresh (no table lock)
CREATE UNIQUE INDEX daily_sales_summary_day_idx
    ON daily_sales_summary (day);

-- Refresh on a schedule, or wire it to pg_cron
REFRESH MATERIALIZED VIEW CONCURRENTLY daily_sales_summary;

-- Check the buffer pool hit ratio (target: >99% for OLTP)
SELECT
    sum(heap_blks_hit) / nullif(sum(heap_blks_hit) + sum(heap_blks_read), 0) AS hit_ratio
FROM pg_statio_user_tables;
