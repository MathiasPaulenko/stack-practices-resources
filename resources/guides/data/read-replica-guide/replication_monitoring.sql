-- PostgreSQL: lag per replica, run on the primary
SELECT
    client_addr,
    state,
    sent_lsn,
    replay_lsn,
    pg_size_pretty(pg_wal_lsn_diff(sent_lsn, replay_lsn)) AS lag
FROM pg_stat_replication;

-- Replica count vs lag: decide if replicas are under-provisioned
SELECT application_name, client_addr,
       pg_wal_lsn_diff(pg_current_wal_lsn(), replay_lsn) AS lag_bytes,
       EXTRACT(EPOCH FROM replay_lag) AS lag_seconds
FROM pg_stat_replication;

-- WAL receiver status, run on the replica itself
SELECT status, receive_start_lsn, written_lsn, flushed_lsn
FROM pg_stat_wal_receiver;

-- Replication slot lag: stalled slots accumulate unconsumed WAL
SELECT slot_name, restart_lsn,
       pg_wal_lsn_diff(pg_current_wal_lsn(), restart_lsn) AS lag_bytes
FROM pg_replication_slots;

-- Hot read queries to route to replicas (pg_stat_statements)
SELECT query, calls, mean_exec_time, total_exec_time
FROM pg_stat_statements
WHERE query LIKE 'SELECT%'
ORDER BY calls DESC
LIMIT 20;

-- MySQL: replica lag — Seconds_Behind_Source (< 5),
-- Replica_IO_Running and Replica_SQL_Running (both Yes)
SHOW REPLICA STATUS;

-- MySQL: replication connection health via performance schema
SELECT
    channel_name,
    service_state,
    last_error_number,
    last_error_message
FROM performance_schema.replication_connection_status;
