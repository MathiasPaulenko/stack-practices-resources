# Deploy Applications to Kubernetes with Helm Charts

Runnable Helm chart covering value overrides, template helpers, lifecycle hooks, subchart dependencies, and a CI/CD deploy workflow.

## Contents

- `myapp/` — complete chart: `Chart.yaml`, `values.yaml`, `values.prod.yaml`, templates, hooks
- `.github/workflows/helm-deploy.yml` — lint + `helm upgrade --install --atomic` pipeline

## Quick start

```bash
helm lint ./myapp
helm template myapp ./myapp -f myapp/values.prod.yaml   # render locally
helm install myapp ./myapp -f myapp/values.prod.yaml   # deploy
helm upgrade --install myapp ./myapp --atomic --wait   # CI-safe upgrade
helm rollback myapp 1                                  # rollback
helm test myapp                                        # run test hooks
```

Source: [Deploy Applications to Kubernetes with Helm Charts](https://stackpractices.com/recipes/helm-chart-deployment/)
