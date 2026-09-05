-- PostgreSQL: Schedule Materialized View Refresh with pg_cron

-- Enable pg_cron extension (requires shared_preload_libraries = 'pg_cron')
CREATE EXTENSION IF NOT EXISTS pg_cron;

-- Schedule a daily refresh at 2 AM
SELECT cron.schedule(
    'refresh_monthly_revenue_daily',
    '0 2 * * *',
    'REFRESH MATERIALIZED VIEW CONCURRENTLY monthly_revenue_mat'
);

-- Schedule a refresh every 15 minutes for near-real-time dashboards
SELECT cron.schedule(
    'refresh_hourly_signups',
    '*/15 * * * *',
    'REFRESH MATERIALIZED VIEW CONCURRENTLY hourly_signups_mat'
);

-- List all scheduled jobs
SELECT jobid, schedule, command, active FROM cron.job;

-- Unschedule a job by name
SELECT cron.unschedule('refresh_monthly_revenue_daily');

-- Unschedule a job by ID
SELECT cron.unschedule(42);
