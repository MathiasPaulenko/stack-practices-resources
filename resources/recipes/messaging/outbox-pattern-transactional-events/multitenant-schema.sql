-- Add tenant_id for multi-tenant isolation
ALTER TABLE outbox_events ADD COLUMN tenant_id VARCHAR(100) NOT NULL;
CREATE INDEX idx_outbox_tenant ON outbox_events (tenant_id, status, created_at);
