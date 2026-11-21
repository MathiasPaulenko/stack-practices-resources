-- PostgreSQL native materialized views: full, concurrent, and trigger-based
-- incremental refresh. Companion code for
-- https://stackpractices.com/patterns/materialized-view-pattern/

-- Create materialized view
CREATE MATERIALIZED VIEW mv_order_summary AS
SELECT
    customer_id,
    COUNT(*) as total_orders,
    SUM(amount) as total_spent,
    MAX(created_at) as last_order_date,
    AVG(amount) as avg_order_value
FROM orders
WHERE status = 'completed'
GROUP BY customer_id;

-- Index for fast lookups (also required for CONCURRENTLY)
CREATE UNIQUE INDEX idx_mv_customer_id ON mv_order_summary(customer_id);

-- Query the view (milliseconds vs seconds on raw tables)
SELECT * FROM mv_order_summary
WHERE customer_id = 12345;

-- Full refresh
REFRESH MATERIALIZED VIEW mv_order_summary;

-- Concurrent refresh (doesn't lock reads)
REFRESH MATERIALIZED VIEW CONCURRENTLY mv_order_summary;

-- Incremental refresh using triggers (manual implementation)
CREATE TABLE mv_customer_summary (
    customer_id INT PRIMARY KEY,
    total_orders INT DEFAULT 0,
    total_spent DECIMAL(12,2) DEFAULT 0,
    last_order_date TIMESTAMP
);

-- Populate initially
INSERT INTO mv_customer_summary
SELECT
    customer_id,
    COUNT(*),
    SUM(amount),
    MAX(created_at)
FROM orders
GROUP BY customer_id;

-- Incremental update trigger
CREATE OR REPLACE FUNCTION refresh_customer_summary()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO mv_customer_summary (customer_id, total_orders, total_spent, last_order_date)
    VALUES (NEW.customer_id, 1, NEW.amount, NEW.created_at)
    ON CONFLICT (customer_id) DO UPDATE SET
        total_orders = mv_customer_summary.total_orders + 1,
        total_spent = mv_customer_summary.total_spent + NEW.amount,
        last_order_date = GREATEST(mv_customer_summary.last_order_date, NEW.created_at);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER order_insert_trigger
AFTER INSERT ON orders
FOR EACH ROW
EXECUTE FUNCTION refresh_customer_summary();
