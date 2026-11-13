# Despliegue de Aplicaciones en Kubernetes con Helm Charts

Helm chart ejecutable con overrides de values, helpers de template, hooks de ciclo de vida, dependencias de subcharts y un workflow de despliegue CI/CD.

## Contenido

- `myapp/` — chart completo: `Chart.yaml`, `values.yaml`, `values.prod.yaml`, templates, hooks
- `.github/workflows/helm-deploy.yml` — pipeline con lint + `helm upgrade --install --atomic`

## Inicio rápido

```bash
helm lint ./myapp
helm template myapp ./myapp -f myapp/values.prod.yaml   # renderiza en local
helm install myapp ./myapp -f myapp/values.prod.yaml   # despliega
helm upgrade --install myapp ./myapp --atomic --wait   # upgrade seguro en CI
helm rollback myapp 1                                  # rollback
helm test myapp                                        # corre los hooks de test
```

Fuente: [Despliegue de Aplicaciones en Kubernetes con Helm Charts](https://stackpractices.com/es/recipes/helm-chart-deployment/)
