-- Foreign keys referencing a partitioned table (PostgreSQL 12+)
-- The partition key must be part of the referenced column set
CREATE TABLE order_items (
  id BIGSERIAL,
  order_id BIGINT NOT NULL,
  order_created_at TIMESTAMPTZ NOT NULL,
  sku TEXT NOT NULL,
  PRIMARY KEY (id, order_created_at),
  FOREIGN KEY (order_id, order_created_at)
    REFERENCES orders (id, created_at)
) PARTITION BY RANGE (order_created_at);

CREATE TABLE order_items_2024_01 PARTITION OF order_items
  FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
