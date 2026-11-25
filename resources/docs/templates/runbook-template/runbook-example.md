## Runbook Example: High CPU on payment-service

This is the template filled in for a real scenario — a Kubernetes alert for elevated CPU on the payments service. Note how every diagnostic step says *what to look for* and every mitigation names the condition that triggers it.

```text
=== Runbook: High CPU on payment-service ===

Alert: PaymentServiceHighCPU
Severity: Warning
Condition: CPU > 80% for 5 minutes

Symptoms:
  - Payment latency increases
  - Request queue grows
  - 5xx errors may appear

Diagnostic Steps:
  1. Check current traffic:
     kubectl top pods -n production -l app=payment
     -> If one pod has significantly higher CPU, it may be a hot spot

  2. Check for errors:
     kubectl logs -n production -l app=payment --tail=100 | grep ERROR
     -> Error loops can cause high CPU

  3. Check DB connections:
     kubectl exec -n production payment-db-0 -- psql -c "SELECT count(*) FROM pg_stat_activity"
     -> Exhausted pool causes retries that consume CPU

  4. Check garbage collection:
     kubectl logs -n production -l app=payment --tail=200 | grep "GC"
     -> Frequent GC indicates memory pressure causing CPU usage

Mitigation Actions:
  A. If it is a hot spot (one pod):
     kubectl scale deployment payment -n production --replicas=+2
     -> Add pods to distribute load

  B. If it is an error loop:
     Identify the error and revert the responsible deploy
     kubectl rollout undo deployment payment -n production

  C. If DB pool is exhausted:
     Increase pool max in config
     kubectl patch configmap payment-config -n production --patch '{"data":{"DB_POOL_MAX":"200"}}'
     kubectl rollout restart deployment payment -n production

  D. If GC pressure:
     Increase pod memory
     kubectl patch deployment payment -n production -p '{"spec":{"template":{"spec":{"containers":[{"name":"payment","resources":{"limits":{"memory":"2Gi"}}}]}}}}'

Post-Mitigation Verification:
  - CPU drops below 60% within 10 minutes
  - p95 latency returns to < 500ms
  - No new 5xx errors
  - Confirm with Grafana dashboard

Escalation:
  - If not resolved in 30 min: escalate to SRE on-call
  - If customer impact: declare SEV2 incident
  - During business hours: contact service owner (Team Payments)

Postmortem:
  - Create postmortem if impact was > 15 min of degradation
  - Identify root cause and create action items
```
