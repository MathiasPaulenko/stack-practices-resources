-- Bad vs good query rewrites. Run each pair with EXPLAIN ANALYZE
-- and compare plans. Requires schema.sql first.

-- ---------- 1. Function on the indexed column → functional index --
-- BAD: LOWER() defeats a plain index on email
SELECT * FROM users WHERE LOWER(email) = 'user5@example.com';

-- GOOD: after CREATE INDEX ON users (LOWER(email)) — see indexes.sql

-- ---------- 2. Implicit type mismatch ------------------------------
-- order_number is VARCHAR; comparing to a number can skip the index.
-- BAD
SELECT * FROM orders WHERE order_number = 12345;
-- GOOD
SELECT * FROM orders WHERE order_number = '12345';

-- ---------- 3. DATE() on the column → range predicate --------------
-- BAD: function wrapping created_at breaks the index
SELECT * FROM orders WHERE DATE(created_at) = CURRENT_DATE - 1;

-- GOOD: half-open range uses the index
SELECT * FROM orders
WHERE created_at >= CURRENT_DATE - 1
  AND created_at <  CURRENT_DATE;

-- ---------- 4. OR across separately-indexed columns → UNION ALL ----
-- BAD: may seq-scan because no single index covers both predicates
SELECT * FROM users
WHERE email = 'user1@example.com' OR name = 'User 2';

-- GOOD: each branch seeks its own index
SELECT * FROM users WHERE email = 'user1@example.com'
UNION ALL
SELECT * FROM users
WHERE name = 'User 2' AND email != 'user1@example.com';

-- ---------- 5. IN on a large subquery → EXISTS ----------------------
-- BAD: materializes the whole subquery result
SELECT * FROM users u
WHERE u.id IN (SELECT o.user_id FROM orders o WHERE o.total > 300);

-- GOOD: stops at the first match per row
SELECT * FROM users u
WHERE EXISTS (
  SELECT 1 FROM orders o
  WHERE o.user_id = u.id AND o.total > 300
);

-- ---------- 6. Correlated subquery per row → JOIN + aggregate ------
-- BAD: one inner query per outer row
SELECT u.name,
       (SELECT COUNT(*) FROM orders o WHERE o.user_id = u.id) AS order_count
FROM users u;

-- GOOD: single pass with a join
SELECT u.name, COUNT(o.id) AS order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.name;

-- ---------- 7. SELECT DISTINCT hiding a join bug --------------------
-- BAD: DISTINCT papers over fan-out from a wrong join
-- SELECT DISTINCT u.name FROM users u JOIN orders o ON u.id = o.user_id;
-- GOOD: fix the join (or use EXISTS) instead of deduplicating after.
SELECT u.name FROM users u
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.user_id = u.id);

-- ---------- 8. COUNT(*) on a huge table → planner estimate ----------
-- BAD in hot paths: exact count scans everything
-- SELECT COUNT(*) FROM orders;
-- GOOD enough: PostgreSQL's planner estimate
SELECT reltuples::bigint AS approx_rows
FROM pg_class WHERE relname = 'orders';
