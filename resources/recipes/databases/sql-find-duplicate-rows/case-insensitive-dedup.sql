-- Case-insensitive deduplication (emails should be compared lowercase)
-- Source: https://stackpractices.com/recipes/sql-find-duplicate-rows/

-- Find case-insensitive duplicate emails
SELECT LOWER(email) AS email_lower, COUNT(*)
FROM users
GROUP BY LOWER(email)
HAVING COUNT(*) > 1;

-- Deduplicate keeping the first occurrence
WITH duplicates AS (
  SELECT id,
         ROW_NUMBER() OVER (PARTITION BY LOWER(email) ORDER BY created_at) AS rn
  FROM users
)
DELETE FROM users
WHERE id IN (SELECT id FROM duplicates WHERE rn > 1);

-- Recommended: enforce uniqueness at the database level with a functional index
CREATE UNIQUE INDEX idx_users_email_lower ON users (LOWER(email));
