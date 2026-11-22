-- Row-Level Security enforces tenant isolation at the database layer
CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL,
    user_id UUID NOT NULL,
    amount DECIMAL(10,2) NOT NULL
);

ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
-- FORCE applies policies to the table owner too — usually your app role
ALTER TABLE orders FORCE ROW LEVEL SECURITY;

-- missing_ok=true returns NULL (and zero rows) when the variable is unset
CREATE POLICY tenant_isolation ON orders
  USING (tenant_id = current_setting('app.current_tenant', true)::UUID);
