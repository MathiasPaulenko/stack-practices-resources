-- Index a lower-cased email for case-insensitive lookups
CREATE INDEX idx_users_email_lower
ON users (LOWER(email));

-- The query must use the same expression to match the index
EXPLAIN ANALYZE
SELECT * FROM users WHERE LOWER(email) = 'alice@example.com';

-- Index a truncated date for monthly reporting
CREATE INDEX idx_orders_month
ON orders (DATE_TRUNC('month', created_at));
