-- PostgreSQL: Views and Materialized Views

-- Regular view: always fresh, runs the query each time
CREATE OR REPLACE VIEW monthly_revenue AS
SELECT
    date_trunc('month', created_at) AS month,
    SUM(amount) AS total
FROM orders
WHERE status = 'completed'
GROUP BY 1;

-- Materialized view: stored on disk, must be refreshed
CREATE MATERIALIZED VIEW monthly_revenue_mat AS
SELECT
    date_trunc('month', created_at) AS month,
    SUM(amount) AS total
FROM orders
WHERE status = 'completed'
GROUP BY 1;

-- Unique index required for CONCURRENTLY refresh
CREATE UNIQUE INDEX idx_monthly_revenue_mat_month
ON monthly_revenue_mat (month);

-- Blocking refresh (locks readers)
REFRESH MATERIALIZED VIEW monthly_revenue_mat;

-- Non-blocking refresh (requires unique index)
REFRESH MATERIALIZED VIEW CONCURRENTLY monthly_revenue_mat;

-- Update planner statistics after refresh
ANALYZE monthly_revenue_mat;

-- Access control: expose only selected columns
CREATE VIEW customer_summary AS
SELECT
    customer_id,
    COUNT(*) AS order_count,
    SUM(total) AS total_spent
FROM orders
WHERE status = 'completed'
GROUP BY customer_id;

GRANT SELECT ON customer_summary TO reporting_role;
REVOKE SELECT ON orders FROM reporting_role;
