-- Safely add NOT NULL, CHECK and FK constraints on a live PostgreSQL table.

-- NOT NULL: add nullable, backfill, then constrain
ALTER TABLE products ADD COLUMN sku VARCHAR(50);
UPDATE products SET sku = CONCAT('SKU-', id) WHERE sku IS NULL;
ALTER TABLE products ALTER COLUMN sku SET NOT NULL;
CREATE UNIQUE INDEX CONCURRENTLY idx_products_sku ON products(sku);

-- CHECK constraint: NOT VALID skips the table scan, validate afterwards
ALTER TABLE orders ADD CONSTRAINT chk_amount CHECK (amount > 0) NOT VALID;
ALTER TABLE orders VALIDATE CONSTRAINT chk_amount;

-- Foreign key: same NOT VALID pattern
ALTER TABLE orders
  ADD CONSTRAINT fk_orders_user
  FOREIGN KEY (user_id) REFERENCES users(id)
  NOT VALID;
ALTER TABLE orders VALIDATE CONSTRAINT fk_orders_user;
