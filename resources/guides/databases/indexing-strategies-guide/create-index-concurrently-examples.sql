-- CREATE INDEX CONCURRENTLY Examples
-- Build indexes without blocking reads or writes in production.
-- These take longer than regular CREATE INDEX but don't lock the table.

-- PostgreSQL: standard concurrent index creation
CREATE INDEX CONCURRENTLY idx_orders_customer_date
  ON orders(customer_id, created_at DESC);

-- PostgreSQL: concurrent partial index
CREATE INDEX CONCURRENTLY idx_orders_pending_date
  ON orders(created_at DESC)
  WHERE status = 'pending';

-- PostgreSQL: concurrent GIN index for full-text search
CREATE INDEX CONCURRENTLY idx_products_fts
  ON products USING GIN(to_tsvector('english', name || ' ' || description));

-- PostgreSQL: concurrent BRIN index for time-series
CREATE INDEX CONCURRENTLY idx_logs_created_brin
  ON logs USING BRIN(created_at);

-- PostgreSQL: concurrent unique index (fails if duplicates exist)
CREATE UNIQUE INDEX CONCURRENTLY idx_users_email_unique
  ON users(email);

-- MySQL 8+: INPLACE algorithm avoids exclusive table locks
ALTER TABLE orders
  ADD INDEX idx_orders_customer_date (customer_id, created_at DESC),
  ALGORITHM=INPLACE, LOCK=NONE;

-- MySQL 8+: INPLACE for a covering index
ALTER TABLE orders
  ADD INDEX idx_orders_customer_total (customer_id, total, status),
  ALGORITHM=INPLACE, LOCK=NONE;

-- Important notes:
-- 1. CONCURRENTLY cannot run inside a transaction block. Don't wrap in BEGIN/COMMIT.
-- 2. If a long-running transaction modifies the table during the build,
--    CONCURRENTLY may fail. Check for long transactions first:
--      SELECT pid, age(now(), xact_start) AS duration, query
--      FROM pg_stat_activity WHERE state = 'active' ORDER BY duration DESC;
-- 3. A failed CONCURRENTLY build leaves an INVALID index. Drop it and retry:
--      DROP INDEX CONCURRENTLY idx_orders_customer_date;
--      CREATE INDEX CONCURRENTLY idx_orders_customer_date ON ...;
