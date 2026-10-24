-- PostgreSQL scheduled purge job
-- Run weekly via pg_cron or external scheduler

-- Purge expired sessions (retention: 30 days)
DELETE FROM sessions
WHERE created_at < NOW() - INTERVAL '30 days';

-- Purge audit logs (retention: 7 years for compliance)
-- DO NOT purge: archived separately

-- Purge deleted user data (retention: 90 days after deletion)
DELETE FROM user_data
WHERE deleted_at IS NOT NULL
  AND deleted_at < NOW() - INTERVAL '90 days';

-- Purge event logs (retention: 180 days)
DELETE FROM event_logs
WHERE created_at < NOW() - INTERVAL '180 days';

-- Vacuum and analyze after purge
VACUUM ANALYZE sessions;
VACUUM ANALYZE user_data;
VACUUM ANALYZE event_logs;
