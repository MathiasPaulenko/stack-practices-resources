-- Deduplication on MySQL 5.7 (no window functions available)
-- Source: https://stackpractices.com/recipes/sql-find-duplicate-rows/

-- Find duplicates
SELECT email, COUNT(*) AS dup_count
FROM users
GROUP BY email
HAVING COUNT(*) > 1;

-- Delete duplicates keeping the row with the lowest id (oldest surrogate key)
DELETE u1 FROM users u1
INNER JOIN users u2
  ON u1.email = u2.email
  AND u1.id > u2.id;

-- Verify: must return zero rows
SELECT email, COUNT(*) FROM users GROUP BY email HAVING COUNT(*) > 1;

-- Prevent recurrence
ALTER TABLE users ADD CONSTRAINT unique_email UNIQUE (email);
