# Runbook: High Error Rate

## Alert: HighErrorRate

- **Severity**: Critical
- **Condition**: Error rate > 5% for 5 minutes
- **Impact**: Users seeing 500 errors

## Quick Triage (5 minutes)

1. Check Grafana dashboard: "API Service Overview"
2. Identify which endpoints have high error rates
3. Check recent deployments: `kubectl rollout history deployment/api -n production`
4. Check pod logs: `kubectl logs -l app=api -n production --tail=100`

## Resolution Steps

### If caused by recent deployment

1. Rollback: `kubectl rollout undo deployment/api -n production`
2. Verify error rate drops: check Grafana
3. Create incident report

### If caused by database issues

1. Check database connections: `kubectl exec -it <db-pod> -- psql -c "SELECT count(*) FROM pg_stat_activity"`
2. Check for long queries: `SELECT pid, now() - query_start AS duration, query FROM pg_stat_activity WHERE state = 'active' ORDER BY duration DESC LIMIT 10`
3. Kill long queries if needed: `SELECT pg_terminate_backend(pid)`

### If caused by external API failure

1. Check external API status page
2. Enable circuit breaker fallback
3. Increase timeout if temporary

## Post-Incident

1. Create postmortem within 48 hours
2. Add alert for earlier detection if possible
3. Update this runbook with new findings
