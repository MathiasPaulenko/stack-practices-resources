-- Materialized views: pre-compute expensive aggregations.
-- PostgreSQL. Requires schema.sql first.

CREATE MATERIALIZED VIEW order_summary AS
SELECT u.id AS user_id, u.name,
       COUNT(o.id) AS total_orders,
       SUM(o.total) AS total_spent,
       MAX(o.created_at) AS last_order_date
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.name;

-- A unique index is REQUIRED before REFRESH ... CONCURRENTLY works.
CREATE UNIQUE INDEX idx_order_summary_user_id ON order_summary (user_id);
CREATE INDEX idx_order_summary_total ON order_summary (total_spent DESC);

-- Fast: reads pre-computed data.
EXPLAIN ANALYZE
SELECT * FROM order_summary ORDER BY total_spent DESC LIMIT 10;

-- Refresh without blocking reads (needs the unique index above).
REFRESH MATERIALIZED VIEW CONCURRENTLY order_summary;

-- Blocking variant (locks readers out during refresh):
-- REFRESH MATERIALIZED VIEW order_summary;

-- ============================ MySQL ================================
-- MySQL has no materialized views. Standard workaround: summary table
-- + scheduled event. Requires SET GLOBAL event_scheduler = ON.
--
-- CREATE TABLE order_summary AS
-- SELECT u.id AS user_id, u.name,
--        COUNT(o.id) AS total_orders,
--        SUM(o.total) AS total_spent,
--        MAX(o.created_at) AS last_order_date
-- FROM users u
-- LEFT JOIN orders o ON u.id = o.user_id
-- GROUP BY u.id, u.name;
--
-- DELIMITER //
-- CREATE EVENT refresh_order_summary
-- ON SCHEDULE EVERY 1 HOUR
-- DO BEGIN
--   TRUNCATE TABLE order_summary;
--   INSERT INTO order_summary
--   SELECT u.id, u.name, COUNT(o.id), SUM(o.total), MAX(o.created_at)
--   FROM users u
--   LEFT JOIN orders o ON u.id = o.user_id
--   GROUP BY u.id, u.name;
-- END //
-- DELIMITER ;
--
-- Multi-statement event bodies need BEGIN ... END — without it the
-- CREATE EVENT fails on the second statement.
