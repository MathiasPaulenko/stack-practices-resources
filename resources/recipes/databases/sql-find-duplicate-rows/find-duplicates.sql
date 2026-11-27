-- Find duplicate rows in a table (PostgreSQL, MySQL, SQL Server, SQLite)
-- Source: https://stackpractices.com/recipes/sql-find-duplicate-rows/

-- Duplicates on a single column
SELECT email, COUNT(*)
FROM users
GROUP BY email
HAVING COUNT(*) > 1;

-- Duplicates across multiple columns
SELECT first_name, last_name, birth_date, COUNT(*) AS dup_count
FROM users
GROUP BY first_name, last_name, birth_date
HAVING COUNT(*) > 1
ORDER BY dup_count DESC;

-- Case-insensitive duplicates (useful for emails)
SELECT LOWER(email) AS email_lower, COUNT(*)
FROM users
GROUP BY LOWER(email)
HAVING COUNT(*) > 1;

-- Duplicates on a JSONB column (PostgreSQL only)
SELECT jsonb_column::text, COUNT(*)
FROM users
GROUP BY jsonb_column::text
HAVING COUNT(*) > 1;
