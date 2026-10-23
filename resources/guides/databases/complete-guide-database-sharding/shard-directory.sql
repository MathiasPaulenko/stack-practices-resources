-- shard_directory.sql
-- Directory table for directory-based sharding (multi-tenant SaaS example).
-- Companion to: https://stackpractices.com/guides/complete-guide-database-sharding/

CREATE TABLE shard_directory (
    tenant_id INT PRIMARY KEY,
    shard_id INT NOT NULL,
    region VARCHAR(20)
);

-- Example seed data: EU tenants on the EU shard, US tenants on the US shard.
INSERT INTO shard_directory (tenant_id, shard_id, region) VALUES
    (1001, 1, 'us-east'),
    (1002, 2, 'eu-west'),
    (1003, 1, 'us-east'),
    (1004, 2, 'eu-west'),
    (1005, 1, 'us-east'),
    (1006, 2, 'eu-west'),
    (1007, 3, 'ap-southeast'),
    (1008, 3, 'ap-southeast');

-- Route lookup executed by the router before each tenant query.
SELECT shard_id FROM shard_directory WHERE tenant_id = 1002;
