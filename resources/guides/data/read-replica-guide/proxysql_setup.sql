-- ProxySQL: hostgroups and query rules for MySQL read/write splitting.
-- hostgroup 0 = writes (primary), hostgroup 1 = reads (replicas).

INSERT INTO mysql_servers(hostgroup_id, hostname, port) VALUES
  (0, 'master.db.internal', 3306),
  (1, 'replica1.db.internal', 3306),
  (1, 'replica2.db.internal', 3306);

-- Locking reads stay on the primary; plain SELECTs fan out to replicas.
INSERT INTO mysql_query_rules(rule_id, active, match_digest, destination_hostgroup, apply)
VALUES
  (1, 1, '^SELECT.*FOR UPDATE', 0, 1),
  (2, 1, '^SELECT', 1, 1);

LOAD MYSQL SERVERS TO RUNTIME;
SAVE MYSQL SERVERS TO DISK;
LOAD MYSQL QUERY RULES TO RUNTIME;
SAVE MYSQL QUERY RULES TO DISK;
