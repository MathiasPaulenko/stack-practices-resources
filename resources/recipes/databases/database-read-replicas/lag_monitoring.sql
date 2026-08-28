-- Replication lag monitoring queries for PostgreSQL and MySQL.
-- Run these on the primary (PostgreSQL) or replica (MySQL).

-- ===== PostgreSQL =====

-- Check replication lag per replica
SELECT
    application_name,
    client_addr,
    state,
    sent_lsn,
    replay_lsn,
    EXTRACT(EPOCH FROM (now() - replay_lag)) AS lag_seconds
FROM pg_stat_replication;

-- Check WAL receiver status on replica
SELECT status, receive_start_lsn, written_lsn, flushed_lsn
FROM pg_stat_wal_receiver;

-- Monitor slot lag (if using replication slots)
SELECT slot_name, restart_lsn,
       pg_wal_lsn_diff(pg_current_wal_lsn(), restart_lsn) AS lag_bytes
FROM pg_replication_slots;

-- Find most frequent read queries (candidates for replica routing)
SELECT query, calls, mean_exec_time, total_exec_time
FROM pg_stat_statements
WHERE query LIKE 'SELECT%'
ORDER BY calls DESC
LIMIT 20;

-- ===== MySQL =====

-- Check replica lag
SHOW REPLICA STATUS\G

-- Key fields to monitor:
-- Seconds_Behind_Master: should be < 5
-- Replica_IO_Running: Yes
-- Replica_SQL_Running: Yes

-- Monitor via performance schema
SELECT
    channel_name,
    service_state,
    last_error_number,
    last_error_message
FROM performance_schema.replication_connection_status;
