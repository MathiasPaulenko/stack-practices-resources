# Helm Chart Templating — Runnable Chart

Companion code for the StackPractices recipe
[Helm Chart Templating: Package Kubernetes Manifests](https://stackpractices.com/recipes/kubernetes-helm-chart-templating/).

## Files

| File | What it shows |
|------|---------------|
| `my-chart/Chart.yaml` | Chart metadata, maintainers, and an OCI subchart dependency (`postgresql`) |
| `my-chart/.helmignore` | Patterns excluded from the packaged `.tgz` |
| `my-chart/values.yaml` | Default values: replicas, image, service, resources, ingress, config, subchart toggles |
| `my-chart/values/staging.yaml` | Staging overrides: RC image tag, debug logs, staging host |
| `my-chart/values/production.yaml` | Production overrides: 5 replicas, higher limits, prod host |
| `my-chart/templates/_helpers.tpl` | Named templates: `name`, `fullname`, `labels`, `selectorLabels` |
| `my-chart/templates/deployment.yaml` | Deployment consuming `.Values`, `.Chart`, and helpers |
| `my-chart/templates/service.yaml` | ClusterIP service matching the deployment selectors |
| `my-chart/templates/configmap.yaml` | ConfigMap built by `range` over `.Values.config` |
| `my-chart/templates/ingress.yaml` | Conditional ingress with `if`, `with`, nested `range`, and `$` scope |
| `my-chart/templates/post-install-job.yaml` | Helm hook Job (post-install/post-upgrade, weighted, auto-cleanup) |
| `my-chart/templates/sealedsecret.yaml` | Conditional Bitnami SealedSecret template |
| `my-chart/templates/NOTES.txt` | Post-install notes rendered with template logic |

## Use

Render the chart without a cluster:

```bash
helm lint my-chart                                            # validate
helm template my-app my-chart                                 # defaults
helm template my-app my-chart -f my-chart/values/production.yaml
```

Install against a real cluster:

```bash
helm install my-app my-chart                                  # defaults (ingress off)
helm install my-app my-chart -f my-chart/values/staging.yaml
helm upgrade my-app my-chart -f my-chart/values/production.yaml
helm rollback my-app 1
```

Package and distribute:

```bash
helm dependency update my-chart   # resolves the OCI postgresql subchart, writes Chart.lock
helm package my-chart             # produces my-chart-1.0.0.tgz
helm push my-chart-1.0.0.tgz oci://registry.example.com/charts
```

The `postgresql` dependency is disabled by default (`postgresql.enabled: false`), so the chart
renders without fetching subcharts. Set it to `true` and run `helm dependency update` to pull it.
