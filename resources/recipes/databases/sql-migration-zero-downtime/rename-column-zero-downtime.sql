-- Expand-contract rename: zero-downtime column rename on a busy table
ALTER TABLE customers ADD COLUMN email_address VARCHAR(255);

CREATE OR REPLACE FUNCTION sync_email() RETURNS TRIGGER AS $$
BEGIN
  IF NEW.email_address IS DISTINCT FROM OLD.email_address THEN
    NEW.email := NEW.email_address;
  ELSIF NEW.email IS DISTINCT FROM OLD.email THEN
    NEW.email_address := NEW.email;
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER customers_sync_email
BEFORE INSERT OR UPDATE ON customers
FOR EACH ROW EXECUTE FUNCTION sync_email();

-- Backfill in batches (see batch-backfill.sql for the full loop)
UPDATE customers
SET email_address = email
WHERE id BETWEEN 1 AND 1000
  AND email_address IS NULL;

-- Verify, then cut over
SELECT COUNT(*) FROM customers WHERE email_address IS DISTINCT FROM email;

ALTER TABLE customers DROP COLUMN email;
ALTER TABLE customers RENAME COLUMN email_address TO email;
DROP TRIGGER customers_sync_email ON customers;
DROP FUNCTION sync_email();
