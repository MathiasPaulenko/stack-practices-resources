# Despliegues Canary con Istio — Código complementario

Manifiestos complementarios de la receta
[Despliegues Canary con Istio Service Mesh](https://stackpractices.com/es/recipes/istio-canary-deployment/).

Una configuración canary completa: ambas versiones de la aplicación, los subsets
de la DestinationRule, el enrutado ponderado del VirtualService, el script de
rollout progresivo, las variantes por cabecera y de espejado, circuit breaking y
un recurso `Canary` de Flagger para promoción automática basada en métricas.

## Archivos

| Archivo | Qué muestra |
|---------|-------------|
| `deployment-v1.yaml` / `deployment-v2.yaml` | Deployments estable y canary con etiquetas `version` |
| `destination-rule.yaml` | Subsets `v1`/`v2` + outlier detection |
| `virtual-service-canary.yaml` | División de tráfico ponderada 90/10 |
| `virtual-service-header-routing.yaml` | Match por cabecera (`x-canary-test`) → v2 para testers |
| `virtual-service-mirror.yaml` | Espejado del 100% del tráfico a v2 (shadow traffic) |
| `destination-rule-circuit-breaker.yaml` | Límites más ajustados + `LEAST_REQUEST` para el pool canary |
| `canary-analysis.yaml` | `Canary` de Flagger: stepWeight 10%, éxito ≥99%, p95 ≤500ms, webhook de carga |
| `canary-rollout.sh` | Rollout progresivo manual: 10% → 50% → 100% con ventanas de monitorización |
| `cleanup-old-version.sh` | Escalado a cero y borrado de v1 tras la promoción completa |

## Uso

```bash
kubectl apply -f deployment-v1.yaml -f deployment-v2.yaml
kubectl apply -f destination-rule.yaml -f virtual-service-canary.yaml
./canary-rollout.sh        # manual, o:
kubectl apply -f canary-analysis.yaml   # automatizado con Flagger
./cleanup-old-version.sh   # tras la promoción completa
```

Requiere un clúster de Kubernetes con Istio (inyección de sidecar habilitada) y,
para la vía automatizada, [Flagger](https://docs.flagger.app/) instalado.
