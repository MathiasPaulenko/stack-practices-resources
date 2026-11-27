-- Migrate a foreign key column without breaking referential integrity
ALTER TABLE orders ADD COLUMN customer_id_new INTEGER;
UPDATE orders SET customer_id_new = customer_id WHERE customer_id_new IS NULL;

ALTER TABLE orders ADD CONSTRAINT fk_orders_customer_new
FOREIGN KEY (customer_id_new) REFERENCES customers(id);

-- After the app uses the new FK:
ALTER TABLE orders DROP CONSTRAINT fk_orders_customer;
ALTER TABLE orders DROP COLUMN customer_id;
ALTER TABLE orders RENAME COLUMN customer_id_new TO customer_id;
