-- Range partitioning by month: the most common layout for time-series data
CREATE TABLE orders (
  id BIGSERIAL,
  customer_id BIGINT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL,
  amount NUMERIC(10,2),
  PRIMARY KEY (id, created_at)  -- partition key must be in the PK
) PARTITION BY RANGE (created_at);

CREATE TABLE orders_2024_01 PARTITION OF orders
  FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

CREATE TABLE orders_2024_02 PARTITION OF orders
  FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');
