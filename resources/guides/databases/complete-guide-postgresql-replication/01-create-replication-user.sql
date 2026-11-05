-- Runs once on first container start (docker-entrypoint-initdb.d).
-- Dedicated replication principal: REPLICATION only, no table access.
CREATE ROLE replicator WITH REPLICATION LOGIN PASSWORD 'change_me_before_production';

-- Slot for the lab replica; the replica uses primary_slot_name='replica1_slot'.
SELECT pg_create_physical_replication_slot('replica1_slot');
