-- monitoring-queries.sql — run against the primary unless noted.

-- 1. Who is streaming and how far behind (bytes + interval lag)
SELECT
  application_name,
  client_addr,
  state,
  sync_state,
  pg_wal_lsn_diff(sent_lsn, replay_lsn) AS lag_bytes,
  write_lag,
  flush_lag,
  replay_lag
FROM pg_stat_replication;

-- 2. Replication slot health — inactive slots with growing retention are a disk risk
SELECT
  slot_name,
  slot_type,
  active,
  wal_status,
  pg_wal_lsn_diff(pg_current_wal_lsn(), restart_lsn) AS retained_bytes
FROM pg_replication_slots;

-- 3. On a replica: is it in recovery, and how stale is the last replay?
SELECT pg_is_in_recovery();
SELECT
  EXTRACT(EPOCH FROM (now() - pg_last_xact_replay_timestamp())) AS lag_seconds,
  pg_last_wal_replay_lsn();
SELECT status, latest_end_lsn, latest_end_time FROM pg_stat_wal_receiver;

-- 4. On a logical subscriber: apply-worker progress
SELECT subname, pid, received_lsn, latest_end_lsn
FROM pg_stat_subscription;

-- 5. On the publisher: lag of each logical slot
SELECT
  slot_name,
  active,
  pg_wal_lsn_diff(pg_current_wal_lsn(), confirmed_flush_lsn) AS lag_bytes
FROM pg_replication_slots
WHERE slot_type = 'logical';
