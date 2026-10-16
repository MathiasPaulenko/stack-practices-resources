# Templating con Helm — Chart ejecutable

Código complementario de la receta de StackPractices
[Templating con Helm: empaquetar manifiestos Kubernetes](https://stackpractices.com/es/recipes/kubernetes-helm-chart-templating/).

## Archivos

| Archivo | Qué muestra |
|---------|-------------|
| `my-chart/Chart.yaml` | Metadata del chart, maintainers y una dependencia de subchart OCI (`postgresql`) |
| `my-chart/.helmignore` | Patrones excluidos del `.tgz` empaquetado |
| `my-chart/values.yaml` | Values por defecto: réplicas, imagen, service, resources, ingress, config, toggles de subchart |
| `my-chart/values/staging.yaml` | Overrides de staging: tag RC de imagen, logs en debug, host de staging |
| `my-chart/values/production.yaml` | Overrides de producción: 5 réplicas, límites más altos, host de prod |
| `my-chart/templates/_helpers.tpl` | Named templates: `name`, `fullname`, `labels`, `selectorLabels` |
| `my-chart/templates/deployment.yaml` | Deployment que consume `.Values`, `.Chart` y helpers |
| `my-chart/templates/service.yaml` | Service ClusterIP que coincide con los selectores del deployment |
| `my-chart/templates/configmap.yaml` | ConfigMap construido con `range` sobre `.Values.config` |
| `my-chart/templates/ingress.yaml` | Ingress condicional con `if`, `with`, `range` anidado y scope `$` |
| `my-chart/templates/post-install-job.yaml` | Job de Helm hook (post-install/post-upgrade, con peso y auto-limpieza) |
| `my-chart/templates/sealedsecret.yaml` | Template condicional de SealedSecret de Bitnami |
| `my-chart/templates/NOTES.txt` | Notas post-install renderizadas con lógica de template |

## Uso

Renderizá el chart sin cluster:

```bash
helm lint my-chart                                            # validar
helm template my-app my-chart                                 # defaults
helm template my-app my-chart -f my-chart/values/production.yaml
```

Instalá contra un cluster real:

```bash
helm install my-app my-chart                                  # defaults (ingress apagado)
helm install my-app my-chart -f my-chart/values/staging.yaml
helm upgrade my-app my-chart -f my-chart/values/production.yaml
helm rollback my-app 1
```

Empaquetá y distribuí:

```bash
helm dependency update my-chart   # resuelve el subchart OCI postgresql, escribe Chart.lock
helm package my-chart             # produce my-chart-1.0.0.tgz
helm push my-chart-1.0.0.tgz oci://registry.example.com/charts
```

La dependencia `postgresql` está deshabilitada por defecto (`postgresql.enabled: false`), así que
el chart renderiza sin descargar subcharts. Ponela en `true` y corré `helm dependency update` para bajarla.
