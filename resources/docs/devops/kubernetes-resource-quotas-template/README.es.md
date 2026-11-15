# Plantilla de Kubernetes Resource Quotas

Recursos companion de la [Plantilla de Kubernetes Resource Quotas](https://stackpractices.com/es/docs/kubernetes-resource-quotas-template/) en StackPractices.

## Archivos

| Archivo | Qué cubre |
|---------|-----------|
| `resourcequota_standard.yaml` | Quota de nivel estándar por namespace: cómputo, almacenamiento y conteo de objetos |
| `limitrange_defaults.yaml` | LimitRange con defaults, cotas y `maxLimitRequestRatio` por contenedor/pod/PVC |
| `quota_tier_small.yaml` | Quota de nivel pequeño (4 CPU / 8Gi / 20 pods) |
| `quota_tier_large.yaml` | Quota de nivel grande (25 CPU / 50Gi / 100 pods) |
| `priorityclasses.yaml` | Cuatro PriorityClasses: critical, high-priority, standard (globalDefault), low-priority |
| `quota_scoped_priority.yaml` | Quotas con alcance por prioridad usando `spec.scopeSelector.matchExpressions` |
| `namespace_bundle.yaml` | Paquete completo de namespace: Namespace + ResourceQuota + LimitRange + NetworkPolicy de denegación |
| `prometheus_quota_alerts.yaml` | Alertas de Prometheus para quota de CPU cercana al límite y quota de memoria excedida |
| `check_quota.sh` | Script de auditoría: quotas, used vs hard, LimitRanges y top de pods |

## Uso

Aplica la quota y su LimitRange juntos: una quota sin defaults rechaza todo pod que omita `resources`:

```bash
kubectl apply -f namespace_bundle.yaml
./check_quota.sh team-payments
```

Para quotas con alcance por prioridad, crea primero las PriorityClasses y luego las porciones de quota. Los pods solo cuentan hacia una quota con alcance cuando definen un `priorityClassName` coincidente.

```bash
kubectl apply -f priorityclasses.yaml
kubectl apply -f quota_scoped_priority.yaml
```

Nunca dimensiones una quota justo al uso actual: las actualizaciones graduales duplican por un momento la huella de un Deployment. Mantén un 20–30% de margen.
