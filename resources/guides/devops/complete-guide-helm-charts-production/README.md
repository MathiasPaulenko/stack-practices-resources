# Helm Charts in Production — Companion Resources

Example chart for the guide
[Helm Charts in Production](https://stackpractices.com/guides/complete-guide-helm-charts-production/).

## Contents

| File | Purpose |
| --- | --- |
| `Chart.yaml` | Chart metadata with pinned dependency |
| `values.yaml` / `values-prod.yaml` | Layered defaults + prod overrides |
| `templates/_helpers.tpl` | Named templates (fullname, labels, SA) |
| `templates/deployment.yaml` | Production deployment template |
| `templates/hooks/post-install-job.yaml` | Migration hook with delete policy |
| `tests/deployment_test.yaml` | helm-unittest assertions |

## Usage

```bash
helm lint .
helm template my-release . -f values-prod.yaml
helm unittest .
helm install my-release . -f values-prod.yaml --atomic --wait
```
