-- Read model projection (SQL)
-- Source: https://stackpractices.com/recipes/cqrs-pattern-recipe/

-- Denormalized read model for order summaries
CREATE TABLE order_summaries (
  order_id UUID PRIMARY KEY,
  customer_name VARCHAR(255),
  total_amount DECIMAL(10,2),
  item_count INT,
  status VARCHAR(20),
  last_updated TIMESTAMP
);

-- Projection handler updates read model when events occur
CREATE OR REPLACE FUNCTION project_order_paid()
RETURNS TRIGGER AS $$
BEGIN
  UPDATE order_summaries
  SET status = 'paid', last_updated = NEW.occurred_at
  WHERE order_id = NEW.aggregate_id;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;
