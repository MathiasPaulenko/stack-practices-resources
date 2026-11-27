-- Dual-write handled by the application instead of a trigger.
-- The app writes to both columns; the DB only backfills and verifies.
ALTER TABLE customers ADD COLUMN email_address VARCHAR(255);

-- App code: every INSERT/UPDATE sets both email and email_address
-- Backfill via the app in batches:
-- UPDATE customers SET email_address = email WHERE id BETWEEN ? AND ?

SELECT COUNT(*) FROM customers WHERE email_address IS DISTINCT FROM email;

-- After switching app reads:
ALTER TABLE customers DROP COLUMN email;
