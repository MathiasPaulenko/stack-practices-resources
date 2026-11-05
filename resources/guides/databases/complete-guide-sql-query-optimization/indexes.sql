-- Index strategies: covering, partial, composite-order, functional, trigram.
-- PostgreSQL syntax unless noted. Requires schema.sql first.

-- ======================== Covering index =========================
-- INCLUDE adds non-key columns to the leaf: the query answers from the
-- index alone (Index Only Scan), never touching the table.
CREATE INDEX idx_users_email_name
  ON users (email) INCLUDE (name, id);

EXPLAIN ANALYZE
SELECT id, name FROM users WHERE email = 'user42@example.com';

-- MySQL equivalent: all needed columns go in the index itself.
-- CREATE INDEX idx_users_email_name ON users (email, name, id);

-- ========================= Partial index ==========================
-- Index only the rows that matter; great for skewed status columns.
CREATE INDEX idx_active_users_email
  ON users (email) WHERE status = 'active';

EXPLAIN ANALYZE
SELECT * FROM users
WHERE status = 'active' AND email = 'user7@example.com';

-- MySQL equivalent: generated column + regular index.
-- ALTER TABLE users ADD COLUMN is_active TINYINT
--   GENERATED ALWAYS AS (IF(status='active',1,NULL)) STORED;
-- CREATE INDEX idx_active_users ON users (is_active, email);

-- ==================== Composite index order =======================
-- Rule: equality columns first, then the sort column, then the range.
CREATE INDEX idx_users_status_created_age
  ON users (status, created_at DESC, age);

-- Serves all three shapes below without a filesort:
EXPLAIN ANALYZE
SELECT * FROM users WHERE status = 'active'
ORDER BY created_at DESC LIMIT 20;

EXPLAIN ANALYZE
SELECT * FROM users WHERE status = 'active' AND age > 18
ORDER BY created_at DESC LIMIT 20;
-- age > 18 is applied as a residual filter: the index removes the sort
-- but cannot seek directly into the matching ages. If the range is very
-- selective, try (status, age, created_at) and compare plans.

-- ======================= Functional index =========================
-- A function on the column defeats a plain index.
EXPLAIN ANALYZE
SELECT * FROM users WHERE LOWER(email) = 'user5@example.com';  -- seq scan

CREATE INDEX idx_users_email_lower ON users (LOWER(email));
-- Re-run the EXPLAIN above: now an index scan.

-- ========================= Trigram index ==========================
-- Leading wildcards cannot seek a B-tree; pg_trgm makes them searchable.
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE INDEX idx_products_name_trgm
  ON products USING gin (name gin_trgm_ops);

EXPLAIN ANALYZE
SELECT * FROM products WHERE name LIKE '%product 12%';

-- ========================= Join columns ===========================
-- Index the join columns on both sides.
CREATE INDEX idx_orders_user_id ON orders (user_id);
CREATE INDEX idx_comments_created_post ON comments (created_at, post_id);
CREATE INDEX idx_order_items_order ON order_items (order_id);

-- ======================== Maintenance =============================
-- pg_prewarm warms a table into the buffer cache after a restart.
CREATE EXTENSION IF NOT EXISTS pg_prewarm;
SELECT pg_prewarm('users');
