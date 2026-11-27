-- Composite partitioning: range by date, then list by region inside
CREATE TABLE sales (
  id BIGSERIAL,
  region TEXT NOT NULL,
  sale_date DATE NOT NULL,
  amount NUMERIC(10,2),
  PRIMARY KEY (id, sale_date, region)
) PARTITION BY RANGE (sale_date);

CREATE TABLE sales_2024_01 PARTITION OF sales
  FOR VALUES FROM ('2024-01-01') TO ('2024-02-01')
  PARTITION BY LIST (region);

CREATE TABLE sales_2024_01_north PARTITION OF sales_2024_01
  FOR VALUES IN ('north', 'northeast');
CREATE TABLE sales_2024_01_south PARTITION OF sales_2024_01
  FOR VALUES IN ('south', 'southeast');
