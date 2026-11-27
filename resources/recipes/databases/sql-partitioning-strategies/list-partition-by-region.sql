-- List partitioning for discrete categories
CREATE TABLE customers (
  id BIGSERIAL,
  name TEXT NOT NULL,
  region TEXT NOT NULL,
  email TEXT,
  PRIMARY KEY (id, region)
) PARTITION BY LIST (region);

CREATE TABLE customers_north PARTITION OF customers
  FOR VALUES IN ('north', 'northeast');
CREATE TABLE customers_south PARTITION OF customers
  FOR VALUES IN ('south', 'southeast');
CREATE TABLE customers_west PARTITION OF customers
  FOR VALUES IN ('west', 'southwest');

-- Catch-all for unexpected regions
CREATE TABLE customers_default PARTITION OF customers DEFAULT;
