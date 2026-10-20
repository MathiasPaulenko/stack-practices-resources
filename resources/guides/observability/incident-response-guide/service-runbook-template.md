# Service Runbook Template

Skeleton for a per-service incident runbook. Adapt the checks to your stack.

```markdown
## Service Runbook: <service-name>

### Symptoms that trigger this runbook
- Alert: <error rate / latency / saturation threshold>
- User reports of <symptom>

### First 5 minutes
1. Confirm scope: which endpoints, which regions, since when?
2. Check the last deploy: `kubectl rollout history deploy/<service>`
3. Check dependencies: database pool, auth service, upstreams
4. Check dashboards: error rate, latency, saturation

### Mitigation ladder (try in order)
1. Rollback the last deploy if it correlates: `kubectl rollout undo`
2. Disable the suspect feature flag
3. Scale replicas if capacity-bound: `kubectl scale --replicas=N`
4. Fail over to the secondary region (requires IC approval)

### Escalation
- Sev1/Sev2: declare incident, page secondary + team lead
- No progress in 30 min: escalate to service owner
- Data corruption suspected: freeze writes, escalate to DBA on-call

### After resolution
- Paste the timeline into the incident ticket
- Schedule postmortem (Sev1/Sev2) within 48h
- Update this runbook with anything you had to discover by hand
```

## Rules that make runbooks work

- Test them in game days — an untested runbook is fiction.
- Update them after every incident that exposed a gap.
- Keep them one click away: linked from the alert, pinned in the service channel.
