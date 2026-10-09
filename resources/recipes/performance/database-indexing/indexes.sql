-- Indexes from the recipe, in the order you'd typically create them.

-- Single-column index
CREATE INDEX idx_users_email ON users(email);

-- Composite index: equality column first, range column second.
-- Serves: WHERE user_id = ?, WHERE user_id = ? AND created_at > ?, ORDER BY user_id, created_at DESC
CREATE INDEX idx_orders_user_created ON orders(user_id, created_at DESC);

-- Partial index: only non-deleted rows (soft-delete pattern)
CREATE INDEX idx_orders_active ON orders(user_id) WHERE deleted_at IS NULL;

-- Covering index (PostgreSQL): INCLUDE keeps extra columns out of the sort key
-- but lets index-only scans answer the query without touching the heap.
CREATE INDEX idx_orders_covering ON orders(user_id, status) INCLUDE (total_amount, created_at);

-- Expression index: case-insensitive email lookup
CREATE INDEX idx_users_lower_email ON users(LOWER(email));

-- Foreign key index (PostgreSQL does not create these automatically)
CREATE INDEX idx_orders_user_id ON orders(user_id);

-- Index matching the sort order for keyset pagination
CREATE INDEX idx_orders_cursor ON orders(created_at DESC, id DESC);
