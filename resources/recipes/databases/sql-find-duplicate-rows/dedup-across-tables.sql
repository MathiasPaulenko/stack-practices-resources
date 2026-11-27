-- Find and remove duplicates that span multiple tables (PostgreSQL, MySQL)
-- Source: https://stackpractices.com/recipes/sql-find-duplicate-rows/

-- Find emails that exist more than once across users and archived_users
SELECT email, COUNT(*)
FROM (
  SELECT email FROM users
  UNION ALL
  SELECT email FROM archived_users
) all_emails
GROUP BY email
HAVING COUNT(*) > 1;

-- Remove from the archive any row that exists in the active table
DELETE FROM archived_users
WHERE email IN (SELECT email FROM users);
