-- SQL Server: Indexed View (Materialized View equivalent)

-- Create the view with SCHEMABINDING
CREATE VIEW dbo.OrderTotals
WITH SCHEMABINDING
AS
SELECT
    o.customer_id,
    COUNT_BIG(*) AS order_count,
    SUM(o.total) AS total_spent
FROM dbo.orders o
WHERE o.status = 'completed'
GROUP BY o.customer_id;
GO

-- Clustered index materializes the view
CREATE UNIQUE CLUSTERED INDEX IX_OrderTotals_Customer
ON dbo.OrderTotals (customer_id);
GO

-- Query the materialized data (NOEXPAND forces using the index)
SELECT * FROM dbo.OrderTotals WITH (NOEXPAND)
WHERE total_spent > 1000;

-- Without NOEXPAND, the optimizer may expand the view to the base query
-- Use NOEXPAND in Standard Edition to guarantee indexed view usage
SELECT customer_id, order_count
FROM dbo.OrderTotals WITH (NOEXPAND)
ORDER BY total_spent DESC;
