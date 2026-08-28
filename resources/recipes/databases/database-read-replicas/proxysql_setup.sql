-- ProxySQL setup for MySQL read/write splitting.
-- Run these queries on the ProxySQL admin interface (port 6032).

-- Configure backend servers
INSERT INTO mysql_servers(hostgroup_id, hostname, port) VALUES
  (0, 'master.db.internal', 3306),   -- hostgroup 0: writes
  (1, 'replica1.db.internal', 3306),  -- hostgroup 1: reads
  (1, 'replica2.db.internal', 3306);  -- hostgroup 1: reads

-- Routing rules: SELECT goes to replicas, everything else to master
INSERT INTO mysql_query_rules(rule_id, active, match_digest, destination_hostgroup, apply)
VALUES
  (1, 1, '^SELECT.*FOR UPDATE', 0, 1),  -- Locking reads to master
  (2, 1, '^SELECT', 1, 1);               -- Regular reads to replicas

LOAD MYSQL SERVERS TO RUNTIME;
SAVE MYSQL SERVERS TO DISK;
LOAD MYSQL QUERY RULES TO RUNTIME;
SAVE MYSQL QUERY RULES TO DISK;
