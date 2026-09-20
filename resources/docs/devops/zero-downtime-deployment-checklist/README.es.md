# Despliegue sin Tiempo de Inactividad — Recursos Complementarios

Archivos complementarios del [Checklist de Despliegue sin Tiempo de Inactividad](https://stackpractices.com/es/docs/zero-downtime-deployment-checklist/) en StackPractices.com.

## Qué incluye

| Archivo | Formato | Descripción |
|---------|---------|-------------|
| `zero-downtime-checklist.md` | Markdown | Checklist imprimible y rellenable — pégalo en un ticket de release y marca cada puerta |
| `rolling-update.yaml` | YAML | Deployment de Kubernetes con `maxUnavailable: 0`, sondas de readiness/liveness y hook `preStop` de drenaje |
| `canary-rollout.yaml` | YAML | Canary de Argo Rollouts con pasos ponderados y puertas de métricas vía `AnalysisTemplate` |

## Inicio rápido

### 1. Copia el checklist en tu ticket de release

```bash
cp zero-downtime-checklist.md releases/$(date +%F)-mi-app-v2.md
```

Rellena los placeholders de la cabecera y marca cada puerta en orden.

### 2. Adapta los manifests

Ambos YAML usan placeholders `<app>`, `<registry>`, `<tag>` y `<namespace>`. El manifest canary espera un `AnalysisTemplate` llamado `success-rate` en el mismo namespace — créalo consultando tu proveedor de métricas (Prometheus, Datadog, CloudWatch) antes del primer rollout.

```bash
kubectl apply -f rolling-update.yaml   # o: kubectl apply -f canary-rollout.yaml
```

## Umbrales de rollback por defecto

| Disparador | Umbral | Acción |
|------------|--------|--------|
| Pico en tasa de errores | > 0,5% durante 2 min | Pausar rollout |
| Latencia | p99 > línea base + 30% durante 5 min | Revertir tráfico |
| Caída en métrica de negocio | > 5% | Rollback inmediato |
| Fallo de health check | > 10% de instancias | Rollback inmediato |
| Incidente P1 | Cualquiera | Rollback y avisar al on-call |

Vincula los umbrales a tus SLOs — un objetivo de disponibilidad del 99,9% tolera una quema de error budget menor que estos valores por defecto.

## Referencias

- [Documentación de Kubernetes sobre rolling updates](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#rolling-update-deployment)
- [Documentación de Argo Rollouts](https://argo-rollouts.readthedocs.io/)
