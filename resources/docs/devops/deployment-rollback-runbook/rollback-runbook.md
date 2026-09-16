# Deployment Rollback Runbook: `<Service Name>`

## Service

- App: `<my-app>` · Namespace: `production` · Deployment method: `kubectl / Helm / ArgoCD / blue-green / canary`
- Last known good version: `<v2.3.0>` · Owner: `@platform-team` · Status page: `<url>`

## 1. Rollback triggers

| Trigger | Severity | Action | Timeline |
|---------|----------|--------|----------|
| Error rate > 5% | Critical | Rollback immediately | < 5 min |
| P99 latency > 5x baseline | Critical | Rollback immediately | < 5 min |
| Health check failures | Critical | Rollback immediately | < 5 min |
| Error rate > 1% | High | Investigate, prepare | < 15 min |
| P99 latency > 2x baseline | High | Rollback if trending | < 15 min |
| OOM kills increasing | High | Rollback if trending | < 10 min |
| Customer complaints > 10 | High | Investigate, prepare | < 15 min |
| Deployment job timeout | Medium | Investigate | < 30 min |

## 2. Rollback commands

```bash
# kubectl
kubectl rollout undo deployment/<my-app> -n production
kubectl rollout undo deployment/<my-app> -n production --to-revision=<N>

# Helm
helm rollback <my-app> <REVISION> -n production --timeout 5m

# ArgoCD — Git revert preferred (`argocd app rollback` is imperative; it fights auto-sync)
git revert <bad-commit-sha> && git push origin main
```

## 3. Verification checklist

- [ ] Health check passes
- [ ] Error rate back to baseline (< 0.1%)
- [ ] P99 latency back to baseline
- [ ] All pods running and ready
- [ ] Database connections healthy
- [ ] Dashboards show normal patterns
- [ ] Logs show no new errors

## 4. Communication

```text
[RESOLVED] Production deployment rollback — <my-app>

Timeline:
  - <HH:MM> UTC: Deployment <version> started
  - <HH:MM> UTC: Error rate increased to <X>%
  - <HH:MM> UTC: Rollback initiated
  - <HH:MM> UTC: Rollback complete

Impact:
  - <user-facing impact, duration, error rate>

Root cause (preliminary):
  - <cause>

Current status:
  - Production running <previous version>; all services healthy
```

## 5. Post-rollback

1. Notify stakeholders (Slack, email, status page)
2. Capture timeline; preserve logs and metrics
3. Do NOT redeploy the same version without a fix
4. Root-cause in staging; post-mortem within 48h
5. Update this runbook with lessons learned
