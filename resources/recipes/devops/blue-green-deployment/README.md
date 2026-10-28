# Blue-Green Deployment

Companion scripts for the [Blue-Green Deployment recipe](https://stackpractices.com/recipes/blue-green-deployment/) on StackPractices.

## Files

| File | What it does |
|---|---|
| `switch-traffic.sh` | Nginx upstream switch to green with automatic rollback on failed health check |
| `monitor-post-switch.sh` | 5-minute post-switch watcher; rolls back on non-200 or error_rate > 1% |
| `blue-green-workflow.yml` | GitHub Actions pipeline: deploy → smoke test → switch → verify → scale down |
| `k8s/service.yaml` | Service that selects `version: blue` or `version: green` |
| `k8s/green-deployment.yaml` | Green Deployment with readiness probe |

## Usage

```bash
# Kubernetes flow
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/green-deployment.yaml
kubectl rollout status deployment/app-green --timeout=120s
kubectl patch svc app-active -p '{"spec":{"selector":{"version":"green"}}}'
./monitor-post-switch.sh

# Nginx flow
./switch-traffic.sh
```

Rollback is always the reverse selector patch — `{"version":"blue"}`.
