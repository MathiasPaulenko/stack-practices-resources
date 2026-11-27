-- Merge data from duplicates into the canonical row before deleting them
-- (PostgreSQL). Useful when duplicates hold different non-null values.
-- Source: https://stackpractices.com/recipes/sql-find-duplicate-rows/

-- 1. Merge valuable data into the canonical (rn = 1) row
WITH duplicates AS (
  SELECT id,
         ROW_NUMBER() OVER (PARTITION BY email ORDER BY created_at) AS rn
  FROM users
),
canonical AS (
  SELECT id FROM duplicates WHERE rn = 1
),
to_delete AS (
  SELECT id FROM duplicates WHERE rn > 1
)
UPDATE users u
SET last_name = COALESCE(
  (SELECT MAX(last_name) FROM users WHERE id IN (SELECT id FROM to_delete) AND email = u.email),
  u.last_name
)
WHERE id IN (SELECT id FROM canonical);

-- 2. Then delete the duplicates (the CTE must be re-declared per statement)
WITH duplicates AS (
  SELECT id,
         ROW_NUMBER() OVER (PARTITION BY email ORDER BY created_at) AS rn
  FROM users
)
DELETE FROM users
WHERE id IN (SELECT id FROM duplicates WHERE rn > 1);
