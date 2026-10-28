# Despliegue Blue-Green

Scripts companion de la [receta de Despliegue Blue-Green](https://stackpractices.com/es/recipes/blue-green-deployment/) en StackPractices.

## Archivos

| Archivo | Qué hace |
|---|---|
| `switch-traffic.sh` | Conmutación del upstream Nginx a green con rollback automático si falla el health check |
| `monitor-post-switch.sh` | Vigilancia de 5 minutos post-conmutación; revierte ante no-200 o error_rate > 1% |
| `blue-green-workflow.yml` | Pipeline de GitHub Actions: despliegue → smoke test → conmutación → verificación → scale down |
| `k8s/service.yaml` | Service que selecciona `version: blue` o `version: green` |
| `k8s/green-deployment.yaml` | Deployment green con readiness probe |

## Uso

```bash
# Flujo Kubernetes
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/green-deployment.yaml
kubectl rollout status deployment/app-green --timeout=120s
kubectl patch svc app-active -p '{"spec":{"selector":{"version":"green"}}}'
./monitor-post-switch.sh

# Flujo Nginx
./switch-traffic.sh
```

El rollback es siempre el patch inverso del selector: `{"version":"blue"}`.
