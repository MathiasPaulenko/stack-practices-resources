# Helm Charts en Producción — Recursos complementarios

Chart de ejemplo para la guía
[Helm Charts en Producción](https://stackpractices.com/es/guides/complete-guide-helm-charts-production/).

## Contenido

| Archivo | Propósito |
| --- | --- |
| `Chart.yaml` | Metadatos del chart con dependencia fijada |
| `values.yaml` / `values-prod.yaml` | Defaults por capas + overrides de prod |
| `templates/_helpers.tpl` | Plantillas con nombre (fullname, labels, SA) |
| `templates/deployment.yaml` | Plantilla de deployment de producción |
| `templates/hooks/post-install-job.yaml` | Hook de migración con delete policy |
| `tests/deployment_test.yaml` | Aserciones helm-unittest |

## Uso

```bash
helm lint .
helm template my-release . -f values-prod.yaml
helm unittest .
helm install my-release . -f values-prod.yaml --atomic --wait
```
