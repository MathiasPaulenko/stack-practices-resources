-- Prometheus query for RPO tracking (replication lag over time)
-- Use in Grafana dashboard
SELECT
  date_trunc('day', timestamp) as day,
  avg(value) as avg_lag_seconds,
  max(value) as max_lag_seconds,
  percentile_cont(0.99) WITHIN GROUP (ORDER BY value) as p99_lag_seconds
FROM prometheus_metrics
WHERE metric_name = 'pg_replication_lag_seconds'
  AND timestamp > now() - interval '90 days'
GROUP BY 1
ORDER BY 1;

-- DR test results over time
SELECT
  test_date,
  rto_target_seconds,
  rto_actual_seconds,
  rpo_target_seconds,
  rpo_actual_seconds,
  CASE
    WHEN rto_actual_seconds <= rto_target_seconds THEN 'PASS'
    ELSE 'FAIL'
  END as rto_status,
  CASE
    WHEN rpo_actual_seconds <= rpo_target_seconds THEN 'PASS'
    ELSE 'FAIL'
  END as rpo_status
FROM dr_test_results
ORDER BY test_date DESC
LIMIT 12;

