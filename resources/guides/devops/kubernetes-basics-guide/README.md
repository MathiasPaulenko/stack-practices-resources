# Kubernetes Basics Guide — Companion Manifests

Apply-ready manifests for the [Kubernetes Basics guide](https://stackpractices.com/guides/kubernetes-basics-guide/) on StackPractices.

## Contents

| File | What it does |
|---|---|
| `pod.yaml` | Minimal single-container Pod with a label and env var |
| `deployment.yaml` | 3-replica Deployment with resource requests/limits |
| `service.yaml` | ClusterIP Service selecting the `app: myapp` pods |
| `configmap.yaml` | ConfigMap with two env-style keys |
| `production-deployment.yaml` | Production-grade Deployment: probes, secret env, anti-affinity, `maxUnavailable: 0` |
| `hpa.yaml` | HorizontalPodAutoscaler scaling the deployment 4–20 on CPU/memory |
| `pdb.yaml` | PodDisruptionBudget keeping `minAvailable: 3` during drains |

## Quickstart (kind / minikube / Docker Desktop)

```bash
kubectl apply -f configmap.yaml
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl get pods -w
kubectl port-forward svc/myapp-service 8080:80   # open http://localhost:8080
```

The `production-*` manifests target a `production` namespace and expect a `db-secret` Secret — they're reference material more than a runnable demo.

## Notes

- Images use `nginx:1.27-alpine` so the basics manifests actually run; the guide examples use `myapp:1.0` as a placeholder.
- The production example keeps `registry.example.com/payment:v2.1.0` — swap in your own image before applying.
