# Estrategias de Despliegue — Recursos complementarios

Ejemplos ejecutables de la guía [Estrategias de Despliegue: Blue-Green, Canary y Rolling](https://stackpractices.com/es/guides/deployment-strategies-guide/).

| Archivo | Qué es | Requisitos |
|---------|--------|------------|
| `flagger-canary.yaml` | Canary automatizado para un `Deployment` de Kubernetes con análisis de métricas y rollback automático | [Flagger](https://flagger.app/) instalado en el clúster, Prometheus para métricas |
| `rollout-canary.yaml` | `Rollout` + `AnalysisTemplate` (CRDs de Argo Rollouts) — canary por etapas con criterios de éxito en Prometheus | Controlador de [Argo Rollouts](https://argoproj.github.io/rollouts/), Prometheus |
| `alb-bluegreen.tf` | Blue-green detrás de un ALB de AWS: dos target groups, regla de listener ponderada y variable `live_target` para cambio/rollback instantáneo | Terraform ≥1.5, provider de AWS |

## Uso

```bash
# Flagger — despliega api primero; el recurso Canary gobierna los releases después
kubectl apply -f flagger-canary.yaml

# Argo Rollouts — cambia la imagen y aplica; el CRD Rollout dirige el despliegue
kubectl apply -f rollout-canary.yaml

# Terraform — el cambio y el rollback son un flip de una variable
terraform plan -var 'live_target=green'   # cambio a green
terraform plan -var 'live_target=blue'    # rollback instantáneo
```

**Notas**

- `Rollout`/`AnalysisTemplate` pertenecen a **Argo Rollouts**, no a Argo CD — una confusión habitual.
- Blue-green dobla la infraestructura a nivel de aplicación. Mantén una única base de datos compartida; los cambios de esquema deben seguir expand-contract.
- Los umbrales del canary son ilustrativos — fíjalos en relación a tu propio baseline de 24h.
