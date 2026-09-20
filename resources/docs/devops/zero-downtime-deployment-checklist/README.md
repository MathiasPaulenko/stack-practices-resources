# Zero-Downtime Deployment — Companion Resources

Companion files for the [Zero-Downtime Deployment Checklist](https://stackpractices.com/docs/zero-downtime-deployment-checklist/) on StackPractices.com.

## What's included

| File | Format | Description |
|------|--------|-------------|
| `zero-downtime-checklist.md` | Markdown | Printable, fillable checklist — paste into a release ticket and check each gate |
| `rolling-update.yaml` | YAML | Kubernetes Deployment with `maxUnavailable: 0`, readiness/liveness probes, and a `preStop` drain hook |
| `canary-rollout.yaml` | YAML | Argo Rollouts canary with weighted steps and `AnalysisTemplate` metric gates |

## Quick start

### 1. Copy the checklist into your release ticket

```bash
cp zero-downtime-checklist.md releases/$(date +%F)-my-app-v2.md
```

Fill in the placeholders at the top and check every gate in order.

### 2. Adapt the manifests

Both YAML files use `<app>`, `<registry>`, `<tag>`, and `<namespace>` placeholders. The canary manifest expects an `AnalysisTemplate` named `success-rate` in the same namespace — create one that queries your metrics provider (Prometheus, Datadog, CloudWatch) before the first rollout.

```bash
kubectl apply -f rolling-update.yaml   # or: kubectl apply -f canary-rollout.yaml
```

## Rollback trigger defaults

| Trigger | Threshold | Action |
|---------|-----------|--------|
| Error rate spike | > 0.5% for 2 min | Pause rollout |
| Latency | p99 > baseline + 30% for 5 min | Roll back traffic |
| Business metric drop | > 5% | Roll back immediately |
| Health check failure | > 10% of instances | Roll back immediately |
| P1 incident | Any | Roll back and page on-call |

Tie thresholds to your SLOs — a 99.9% availability target tolerates a shorter error-budget burn than these defaults.

## References

- [Kubernetes rolling update documentation](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#rolling-update-deployment)
- [Argo Rollouts documentation](https://argo-rollouts.readthedocs.io/)
