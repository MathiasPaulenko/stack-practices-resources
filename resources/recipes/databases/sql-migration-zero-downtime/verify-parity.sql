-- Run before cutover: both columns must match on every row
SELECT COUNT(*) AS mismatch_count
FROM customers
WHERE email_address IS DISTINCT FROM email;

SELECT COUNT(*) AS null_count
FROM customers
WHERE email_address IS NULL;

-- Sample mismatched rows for manual inspection
SELECT id, email, email_address
FROM customers
WHERE email_address IS DISTINCT FROM email
LIMIT 10;
