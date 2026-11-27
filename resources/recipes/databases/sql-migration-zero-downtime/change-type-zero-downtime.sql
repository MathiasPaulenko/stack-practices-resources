-- Change a data type with zero downtime (example: dollars -> cents)
ALTER TABLE orders ADD COLUMN total_cents INTEGER;

CREATE OR REPLACE FUNCTION sync_total() RETURNS TRIGGER AS $$
BEGIN
  IF NEW.total_cents IS DISTINCT FROM OLD.total_cents THEN
    NEW.total := NEW.total_cents / 100.0;
  ELSIF NEW.total IS DISTINCT FROM OLD.total THEN
    NEW.total_cents := (NEW.total * 100)::INTEGER;
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER orders_sync_total
BEFORE INSERT OR UPDATE ON orders
FOR EACH ROW EXECUTE FUNCTION sync_total();

-- Backfill with casting
UPDATE orders
SET total_cents = (total * 100)::INTEGER
WHERE id BETWEEN 1 AND 5000
  AND total_cents IS NULL;

-- Verify
SELECT COUNT(*) FROM orders WHERE total_cents IS NULL;
SELECT COUNT(*) FROM orders WHERE total_cents != (total * 100)::INTEGER;

-- Constraint + cutover
ALTER TABLE orders ADD CONSTRAINT chk_total_cents CHECK (total_cents >= 0);
ALTER TABLE orders DROP COLUMN total;
ALTER TABLE orders RENAME COLUMN total_cents TO total;
DROP TRIGGER orders_sync_total ON orders;
DROP FUNCTION sync_total();
