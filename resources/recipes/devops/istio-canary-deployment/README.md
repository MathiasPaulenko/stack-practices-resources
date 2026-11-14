# Canary Deployments with Istio — Companion Code

Companion manifests for the recipe
[Canary Deployments with Istio Service Mesh](https://stackpractices.com/recipes/istio-canary-deployment/).

A complete canary setup: both application versions, the DestinationRule subsets,
weighted VirtualService routing, the progressive rollout script, header-based and
mirroring variants, circuit breaking, and a Flagger `Canary` resource for
automated metric-gated promotion.

## Files

| File | What it shows |
|------|---------------|
| `deployment-v1.yaml` / `deployment-v2.yaml` | Stable and canary Deployments with `version` labels |
| `destination-rule.yaml` | `v1`/`v2` subsets + outlier detection |
| `virtual-service-canary.yaml` | 90/10 weighted traffic split |
| `virtual-service-header-routing.yaml` | Header match (`x-canary-test`) → v2 for testers |
| `virtual-service-mirror.yaml` | 100% traffic mirroring to v2 (shadow traffic) |
| `destination-rule-circuit-breaker.yaml` | Tighter limits + `LEAST_REQUEST` for the canary pool |
| `canary-analysis.yaml` | Flagger `Canary`: stepWeight 10%, success-rate ≥99%, p95 ≤500ms, load-test webhook |
| `canary-rollout.sh` | Manual progressive rollout: 10% → 50% → 100% with monitoring windows |
| `cleanup-old-version.sh` | Scale-down and deletion of v1 after full promotion |

## Usage

```bash
kubectl apply -f deployment-v1.yaml -f deployment-v2.yaml
kubectl apply -f destination-rule.yaml -f virtual-service-canary.yaml
./canary-rollout.sh        # manual, or:
kubectl apply -f canary-analysis.yaml   # automated via Flagger
./cleanup-old-version.sh   # after full promotion
```

Requires a Kubernetes cluster with Istio (sidecar injection enabled) and,
for the automated path, [Flagger](https://docs.flagger.app/) installed.
