# Kubernetes Resource Quotas Template

Companion resources for the [Kubernetes Resource Quotas Template](https://stackpractices.com/docs/kubernetes-resource-quotas-template/) on StackPractices.

## Files

| File | What it covers |
|------|----------------|
| `resourcequota_standard.yaml` | Standard-tier namespace quota: compute, storage, and object counts |
| `limitrange_defaults.yaml` | LimitRange with container/pod/PVC defaults, bounds, and `maxLimitRequestRatio` |
| `quota_tier_small.yaml` | Small-tier quota (4 CPU / 8Gi / 20 pods) |
| `quota_tier_large.yaml` | Large-tier quota (25 CPU / 50Gi / 100 pods) |
| `priorityclasses.yaml` | Four PriorityClasses: critical, high-priority, standard (globalDefault), low-priority |
| `quota_scoped_priority.yaml` | Priority-scoped quotas using `spec.scopeSelector.matchExpressions` |
| `namespace_bundle.yaml` | Full namespace bundle: Namespace + ResourceQuota + LimitRange + deny-all NetworkPolicy |
| `prometheus_quota_alerts.yaml` | Prometheus alerts for CPU quota near-limit and memory quota exceeded |
| `check_quota.sh` | Quota audit script: quotas, used vs hard, LimitRanges, top pods |

## Usage

Apply the quota and its LimitRange together — a quota without defaults rejects every pod that omits `resources`:

```bash
kubectl apply -f namespace_bundle.yaml
./check_quota.sh team-payments
```

For priority-scoped quotas, create the PriorityClasses first, then the scoped quota slices. Pods only count toward a scoped quota when they set a matching `priorityClassName`.

```bash
kubectl apply -f priorityclasses.yaml
kubectl apply -f quota_scoped_priority.yaml
```

Never size a quota to exactly current usage — rolling updates briefly double a Deployment's footprint. Keep 20–30% headroom.
