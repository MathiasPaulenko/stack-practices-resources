# Runbook: ServiceDown

### Alert
ServiceDown: `{{ $labels.job }}` is down

### Impact
Users cannot access `{{ $labels.job }}`. Revenue impact if payment or API.

### Diagnosis Steps
1. Check service health endpoint: `curl http://{{ $labels.instance }}/health`
2. Check if pod is running: `kubectl get pods -l app={{ $labels.job }}`
3. Check recent deployments: `kubectl rollout history deployment/{{ $labels.job }}`
4. Check resource usage: `kubectl top pod -l app={{ $labels.job }}`
5. Check logs: `kubectl logs -l app={{ $labels.job }} --tail=100`

### Resolution Steps
1. If pod crashed: `kubectl rollout restart deployment/{{ $labels.job }}`
2. If resource exhausted: scale deployment or node pool
3. If deployment caused issue: `kubectl rollout undo deployment/{{ $labels.job }}`
4. If dependency down: check dependency status and escalate to owning team

### Escalation
If unresolved in 15 minutes, escalate to: platform-team@company.com
