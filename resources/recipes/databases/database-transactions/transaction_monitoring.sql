-- Transaction and lock monitoring queries for PostgreSQL.

-- Transactions that are idle and still holding locks
SELECT
    pid,
    state,
    now() - query_start AS duration,
    query
FROM pg_stat_activity
WHERE state = 'idle in transaction'
ORDER BY duration DESC;

-- Terminate sessions idle in transaction for more than 5 minutes
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE state = 'idle in transaction'
  AND now() - query_start > interval '5 minutes';

-- Blocked transactions and their blockers
SELECT
    bl.pid AS blocked_pid,
    kl.pid AS blocking_pid,
    a.query AS blocked_query,
    ka.query AS blocking_query
FROM pg_locks bl
JOIN pg_stat_activity a ON bl.pid = a.pid
JOIN pg_locks kl ON bl.locktype = kl.locktype
    AND bl.database IS NOT DISTINCT FROM kl.database
    AND bl.relation IS NOT DISTINCT FROM kl.relation
    AND bl.pid != kl.pid
JOIN pg_stat_activity ka ON kl.pid = ka.pid
WHERE NOT bl.granted;

-- Per-database transaction rates (commits, rollbacks, deadlocks)
SELECT datname, xact_commit, xact_rollback, deadlocks
FROM pg_stat_database
WHERE datname = current_database();

-- Fail fast instead of queueing on a lock forever
SET lock_timeout = '5s';
