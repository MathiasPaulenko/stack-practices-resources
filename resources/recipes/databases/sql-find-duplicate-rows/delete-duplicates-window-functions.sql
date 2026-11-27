-- Delete duplicate rows with ROW_NUMBER (PostgreSQL, MySQL 8+, SQLite 3.25+, SQL Server)
-- Source: https://stackpractices.com/recipes/sql-find-duplicate-rows/

-- 1. Preview: see what will be kept and what will be deleted
WITH duplicates AS (
  SELECT id, email, created_at,
         ROW_NUMBER() OVER (PARTITION BY email ORDER BY created_at) AS rn
  FROM users
)
SELECT
  id,
  email,
  created_at,
  CASE WHEN rn = 1 THEN 'KEEP' ELSE 'DELETE' END AS action
FROM duplicates
ORDER BY email, rn;

-- 2. Safe deletion inside a transaction, with a backup of the removed rows
BEGIN;

CREATE TEMP TABLE dup_backup AS
WITH duplicates AS (
  SELECT id,
         ROW_NUMBER() OVER (PARTITION BY email ORDER BY created_at) AS rn
  FROM users
)
SELECT u.* FROM users u
JOIN duplicates d ON u.id = d.id
WHERE d.rn > 1;

WITH duplicates AS (
  SELECT id,
         ROW_NUMBER() OVER (PARTITION BY email ORDER BY created_at) AS rn
  FROM users
)
DELETE FROM users
WHERE id IN (SELECT id FROM duplicates WHERE rn > 1);

-- 3. Verify: must return zero rows before committing
SELECT email, COUNT(*) FROM users GROUP BY email HAVING COUNT(*) > 1;

COMMIT;
-- If duplicates remain, ROLLBACK;

-- 4. Prevent recurrence once the table is clean
ALTER TABLE users ADD CONSTRAINT unique_email UNIQUE (email);
-- Or, if you want easier rollback later:
-- CREATE UNIQUE INDEX idx_users_unique_email ON users (email);
