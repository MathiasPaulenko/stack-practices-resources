-- Partitioning: partition pruning shrinks what each query scans.
-- PostgreSQL declarative partitioning. Standalone (does not need schema.sql).

-- ====================== Range partition (time) =====================
DROP TABLE IF EXISTS orders_partitioned CASCADE;

CREATE TABLE orders_partitioned (
  id BIGSERIAL,
  user_id BIGINT NOT NULL,
  total DECIMAL(10,2),
  status VARCHAR(20),
  created_at TIMESTAMP NOT NULL
) PARTITION BY RANGE (created_at);

CREATE TABLE orders_p_2026_01 PARTITION OF orders_partitioned
  FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');
CREATE TABLE orders_p_2026_02 PARTITION OF orders_partitioned
  FOR VALUES FROM ('2026-02-01') TO ('2026-03-01');
CREATE TABLE orders_p_2026_03 PARTITION OF orders_partitioned
  FOR VALUES FROM ('2026-03-01') TO ('2026-04-01');

-- Seed each partition so pruning is visible in the plan.
INSERT INTO orders_partitioned (user_id, total, status, created_at)
SELECT i, i * 1.5, 'completed', '2026-01-15'::timestamp + (i || ' minutes')::interval
FROM generate_series(1, 1000) AS i;
INSERT INTO orders_partitioned (user_id, total, status, created_at)
SELECT i, i * 1.5, 'completed', '2026-02-15'::timestamp + (i || ' minutes')::interval
FROM generate_series(1, 1000) AS i;
INSERT INTO orders_partitioned (user_id, total, status, created_at)
SELECT i, i * 1.5, 'completed', '2026-03-15'::timestamp + (i || ' minutes')::interval
FROM generate_series(1, 1000) AS i;

ANALYZE orders_partitioned;

-- Only the February partition appears in the plan.
EXPLAIN (ANALYZE, COSTS OFF)
SELECT * FROM orders_partitioned
WHERE created_at >= '2026-02-01' AND created_at < '2026-03-01';

-- ====================== List partition (category) ===================
DROP TABLE IF EXISTS products_partitioned CASCADE;

CREATE TABLE products_partitioned (
  id BIGSERIAL,
  name VARCHAR(255),
  category VARCHAR(50) NOT NULL,
  price DECIMAL(10,2)
) PARTITION BY LIST (category);

CREATE TABLE products_p_electronics PARTITION OF products_partitioned
  FOR VALUES IN ('electronics', 'computers');
CREATE TABLE products_p_books PARTITION OF products_partitioned
  FOR VALUES IN ('books', 'media');
CREATE TABLE products_p_other PARTITION OF products_partitioned DEFAULT;

INSERT INTO products_partitioned (name, category, price)
SELECT 'P' || i,
       CASE WHEN i % 3 = 0 THEN 'electronics'
            WHEN i % 3 = 1 THEN 'books'
            ELSE 'garden' END,
       i + 0.99
FROM generate_series(1, 900) AS i;

ANALYZE products_partitioned;

-- Only products_p_electronics is scanned.
EXPLAIN (ANALYZE, COSTS OFF)
SELECT * FROM products_partitioned WHERE category = 'electronics';

-- Rule of thumb: partition on the column your queries filter by —
-- almost always created_at. Partitioning on a column nobody filters
-- buys maintenance cost with zero pruning benefit.
