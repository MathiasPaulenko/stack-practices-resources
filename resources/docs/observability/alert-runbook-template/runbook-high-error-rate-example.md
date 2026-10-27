# Alert Runbook: HighErrorRate-PaymentService

## Alert Metadata

| Field | Value |
|-------|-------|
| Alert Name | HighErrorRate-PaymentService |
| Severity | Critical (P1) |
| Alert Source | Prometheus / Alertmanager |
| Alert Query | `rate(http_requests_total{service="payment",status=~"5.."}[5m]) / rate(http_requests_total{service="payment"}[5m]) > 0.05` |
| Trigger Condition | Error rate > 5% for 5 minutes |
| Routing | PagerDuty → Payment Team On-Call |
| Runbook Owner | Payment Team |
| Last Reviewed | 2026-07-05 |
| Last Updated | 2026-07-05 |

## Impact Assessment

| User Impact | Business Impact |
|-------------|-----------------|
| Users can't complete payments | Revenue loss ~$2,000/min during peak |
| Checkout page shows error message | Customer support tickets increase |
| Retry attempts may succeed for transient errors | Reputation damage if prolonged |

## Triage (0-2 minutes)

### Step 1: Acknowledge the Alert

- [ ] Acknowledge in PagerDuty within 2 minutes
- [ ] Post in `#payment-incidents` Slack channel: "Investigating HighErrorRate-PaymentService"
- [ ] Check if this is a known false positive (check recent alert history)

### Step 2: Assess Severity

| Question | If Yes |
|----------|--------|
| Is error rate > 20%? | Escalate to P0, page secondary on-call |
| Is this during peak hours (9-18 UTC)? | Higher priority, revenue impact is greater |
| Are there related alerts firing? | Check for cascade — may be a shared dependency |
| Is this a new deployment? | Check #deployments channel for recent release |
| Is this a known maintenance window? | Check #maintenance channel |

### Step 3: Quick Checks

| Check | How | Expected |
|-------|-----|----------|
| Service health | `curl https://api.example.com/health` | 200 OK |
| Recent deployment | Check `#deployments` channel | Last deploy > 30 min ago |
| Database connectivity | Check Grafana → Payment DB panel | Connections < 80% pool |
| Payment provider status | Check https://status.stripe.com | All systems operational |
| Error logs | `kubectl logs -l app=payment --tail=100` | Look for repeated error patterns |

## Diagnosis (2-15 minutes)

### Step 4: Identify Error Type

| Error Pattern | Likely Cause | Next Step |
|---------------|-------------|-----------|
| 500 Internal Server Error | Application bug or unhandled exception | Go to Step 5A |
| 502 Bad Gateway | Service is down or not responding | Go to Step 5B |
| 503 Service Unavailable | Pod crashes or OOM kills | Go to Step 5C |
| 504 Gateway Timeout | Database slowness or external API timeout | Go to Step 5D |
| 429 Too Many Requests | Rate limiting from payment provider | Go to Step 5E |

### Step 5A: Application Bug (500 Errors)

1. Check error logs for stack traces:
   ```bash
   kubectl logs -l app=payment --tail=200 | grep -A 20 "Error\|Exception\|stack"
   ```
2. Search for the error in Sentry
3. Check if a new code deployment introduced the bug:
   ```bash
   kubectl rollout history deployment/payment
   ```
4. If new deployment caused the error, roll back:
   ```bash
   kubectl rollout undo deployment/payment
   ```
5. Verify error rate drops after rollback

### Step 5B: Service Down (502 Errors)

1. Check pod status:
   ```bash
   kubectl get pods -l app=payment -o wide
   ```
2. Check pod events:
   ```bash
   kubectl describe pod <pod-name> | tail -30
   ```
3. Check if pods are crashing:
   ```bash
   kubectl get events --field-selector reason=BackOff --sort-by=.lastTimestamp | tail -10
   ```
4. If pods are crashing, check crash logs:
   ```bash
   kubectl logs <pod-name> --previous
   ```
5. If all pods are down, restart the deployment:
   ```bash
   kubectl rollout restart deployment/payment
   ```
6. Monitor pod startup and health check

### Step 5C: OOM Kills (503 Errors)

1. Check for OOM kills:
   ```bash
   kubectl get pods -l app=payment -o jsonpath="{.items[*].status.containerStatuses[0].lastState.terminated.reason}"
   ```
2. If OOMKilled, check memory usage in Grafana
3. Check for memory leak in application:
   ```bash
   kubectl top pods -l app=payment --sort-by=memory
   ```
4. Temporary fix: increase memory limit:
   ```bash
   kubectl patch deployment payment -p '{"spec":{"template":{"spec":{"containers":[{"name":"payment","resources":{"limits":{"memory":"1Gi"}}}]}}}}'
   ```
5. Long-term fix: investigate memory leak, file a bug

### Step 5D: Database Timeout (504 Errors)

1. Check database connection pool
2. Check slow queries in database:
   ```sql
   SELECT query, mean_exec_time, calls
   FROM pg_stat_statements
   ORDER BY mean_exec_time DESC
   LIMIT 10;
   ```
3. Check database CPU and IOPS in Grafana
4. If database is overloaded, check for long-running transactions:
   ```sql
   SELECT pid, now() - xact_start AS duration, query, state
   FROM pg_stat_activity
   WHERE state IN ('active', 'idle in transaction')
   ORDER BY duration DESC;
   ```
5. Kill long-running queries if blocking:
   ```sql
   SELECT pg_terminate_backend(<pid>);
   ```

### Step 5E: Rate Limiting (429 Errors)

1. Check the payment provider API dashboard for rate limit warnings
2. Check if request volume spiked:
   ```bash
   kubectl logs -l app=payment --tail=500 | grep "stripe.com" | wc -l
   ```
3. Enable request batching if available
4. Implement client-side rate limiting
5. If the provider is the bottleneck, use idempotency keys to retry safely

## Mitigation (5-30 minutes)

### Quick Mitigation Options

| Option | When to Use | Impact | Reversibility |
|--------|-------------|--------|---------------|
| Roll back deployment | New deploy caused errors | Loses new features | Easy — redeploy |
| Scale up pods | High traffic overwhelming service | Higher cost | Easy — scale down |
| Enable circuit breaker | External API is down | Degrades gracefully | Easy — flip flag |
| Enable fallback mode | Database is slow | Read-only mode | Easy — flip flag |
| Rate limit users | Protecting from DDoS | Some users blocked | Easy — remove limit |
| Disable problematic endpoint | One endpoint causing cascade | Feature unavailable | Easy — re-enable |

## Escalation

| Level | Who | When to Escalate |
|-------|-----|------------------|
| 1 | On-call engineer | Alert received |
| 2 | Secondary on-call | No progress after 15 minutes |
| 3 | Team lead + SRE | No progress after 30 minutes |
| 4 | Engineering manager | Incident > 1 hour or revenue impact > $10k |
| 5 | CTO + VP Engineering | Incident > 4 hours or public impact |

## Resolution

### Step 6: Verify Resolution

- [ ] Error rate below 1% for 10 consecutive minutes
- [ ] No new error alerts firing
- [ ] Payment success rate back to normal (> 99%)
- [ ] No user complaints in #support channel
- [ ] All pods healthy and stable

### Step 7: Document

- [ ] Update incident in PagerDuty with resolution summary
- [ ] Post resolution in `#payment-incidents`: "Resolved: HighErrorRate-PaymentService — <brief summary>"
- [ ] Create postmortem document if P1 (within 48 hours)
- [ ] File follow-up tickets for root cause fix
- [ ] Update this runbook with any new learnings
