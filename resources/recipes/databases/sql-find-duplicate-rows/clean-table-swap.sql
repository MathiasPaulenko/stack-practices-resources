-- Full-table deduplication via a clean copy + atomic swap (PostgreSQL)
-- Best option when a huge portion of the table is duplicated.
-- Source: https://stackpractices.com/recipes/sql-find-duplicate-rows/

-- 1. Create a clean copy: DISTINCT ON keeps one row per email
CREATE TABLE users_clean AS
SELECT DISTINCT ON (email) *
FROM users
ORDER BY email, created_at;

-- 2. Verify row counts match expectations
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM users_clean;

-- 3. Swap tables in a transaction
BEGIN;
DROP TABLE users;
ALTER TABLE users_clean RENAME TO users;
COMMIT;

-- Note: re-create indexes, constraints, sequences and grants afterwards,
-- and make sure no foreign keys reference the old table before dropping it.
