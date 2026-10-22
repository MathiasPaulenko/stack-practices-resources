-- AP-side Cassandra schema: notifications table (write-heavy workload).
-- NetworkTopologyStrategy with RF=3 per datacenter + LOCAL_QUORUM writes
-- keeps the service available during a DC partition; hinted handoff and
-- repair reconcile afterwards.

CREATE KEYSPACE IF NOT EXISTS notifications WITH replication = {
    'class': 'NetworkTopologyStrategy',
    'dc1': 3,
    'dc2': 3,
    'dc3': 3
};

USE notifications;

CREATE TABLE IF NOT EXISTS notifications (
    user_id UUID,
    notification_id TIMEUUID,
    type TEXT,
    payload TEXT,
    read BOOLEAN,
    created_at TIMESTAMP,
    PRIMARY KEY (user_id, notification_id)
) WITH CLUSTERING ORDER BY (notification_id DESC);

-- Tunable consistency per query:
--   LOCAL_QUORUM  -> consistent within the local DC
--   LOCAL_ONE     -> fastest, may be stale
--   EACH_QUORUM   -> strongest, slowest across DCs
