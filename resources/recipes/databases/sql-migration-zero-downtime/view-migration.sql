-- Rename a column behind a view so old queries keep working
ALTER TABLE customers ADD COLUMN email_new VARCHAR(255);
UPDATE customers SET email_new = email WHERE email_new IS NULL;

CREATE OR REPLACE VIEW customers_v1 AS
SELECT id, name, email_new AS email, created_at
FROM customers;

-- Migrate the app to read customers_v1, then:
ALTER TABLE customers DROP COLUMN email;
ALTER TABLE customers RENAME COLUMN email_new TO email;
DROP VIEW customers_v1;
