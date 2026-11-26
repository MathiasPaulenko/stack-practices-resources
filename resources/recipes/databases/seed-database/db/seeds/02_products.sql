INSERT INTO products (sku, name, price, stock)
VALUES
  ('SKU-001', 'Wireless Mouse', 29.99, 150),
  ('SKU-002', 'Mechanical Keyboard', 89.99, 75),
  ('SKU-003', 'USB-C Hub', 49.99, 200)
ON CONFLICT (sku) DO NOTHING;
