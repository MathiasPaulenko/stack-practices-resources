-- Validate new data without locking the table for a full scan
ALTER TABLE orders ADD COLUMN total_cents INTEGER;
UPDATE orders SET total_cents = (total * 100)::INTEGER WHERE total_cents IS NULL;

-- NOT VALID: no table scan, no long lock — new rows are checked immediately
ALTER TABLE orders ADD CONSTRAINT chk_total_cents_positive
CHECK (total_cents >= 0) NOT VALID;

-- Later: validate existing rows (brief lock only)
ALTER TABLE orders VALIDATE CONSTRAINT chk_total_cents_positive;
