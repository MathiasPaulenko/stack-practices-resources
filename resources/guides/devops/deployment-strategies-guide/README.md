# Deployment Strategies — Companion Resources

Runnable examples from the guide [Deployment Strategies: Blue-Green, Canary & Rolling Compared](https://stackpractices.com/guides/deployment-strategies-guide/).

| File | What it is | Requirements |
|------|------------|--------------|
| `flagger-canary.yaml` | Automated canary for a Kubernetes `Deployment` with metric analysis and auto-rollback | [Flagger](https://flagger.app/) installed in the cluster, Prometheus for metrics |
| `rollout-canary.yaml` | `Rollout` + `AnalysisTemplate` (Argo Rollouts CRDs) — staged canary with Prometheus success criteria | [Argo Rollouts](https://argoproj.github.io/rollouts/) controller, Prometheus |
| `alb-bluegreen.tf` | Blue-green behind an AWS ALB: two target groups, weighted listener rule, `live_target` variable for instant cutover/rollback | Terraform ≥1.5, AWS provider |

## Usage

```bash
# Flagger — deploy api first, then the Canary resource takes over releases
kubectl apply -f flagger-canary.yaml

# Argo Rollouts — replace the image and apply; the Rollout CRD drives the rollout
kubectl apply -f rollout-canary.yaml

# Terraform — cutover and rollback are single-variable flips
terraform plan -var 'live_target=green'   # cutover to green
terraform plan -var 'live_target=blue'    # instant rollback
```

**Notes**

- `Rollout`/`AnalysisTemplate` belong to **Argo Rollouts**, not Argo CD — a common confusion.
- Blue-green doubles application-layer infra. Keep a single shared database; schema changes must follow expand-contract.
- The canary thresholds are illustrative — set them relative to your own 24h baseline.
