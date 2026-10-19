# Plantilla de Pod Disruption Budget de Kubernetes

Recursos de apoyo de la [Plantilla de Pod Disruption Budget de Kubernetes](https://stackpractices.com/es/docs/kubernetes-pod-disruption-budget-template/) en StackPractices.

## Archivos

| Archivo | Qué cubre |
|---------|-----------|
| `pdb_minavailable.yaml` | PDB estándar con piso fijo `minAvailable` |
| `pdb_maxunavailable.yaml` | PDB con `maxUnavailable: 1` — el default más sensato para la mayoría de servicios |
| `pdb_percentage.yaml` | PDB porcentual que escala con el número de réplicas (ideal con HPA) |
| `pdb_statefulset.yaml` | PDB consciente de quorum para StatefulSets (bases de datos, etcd) |
| `helm_pdb_template.yaml` | Bloque PDB para el directorio `templates/` de un Helm chart |
| `prometheus_pdb_alerts.yaml` | Reglas de Prometheus para drains bloqueados y presupuestos degradados |
| `drain_node.sh` | Script de drenaje que muestra los PDBs bloqueantes antes de drenar |

## Uso

Aplica un PDB antes de drenar cualquier nodo:

```bash
kubectl apply -f pdb_maxunavailable.yaml
kubectl get pdb -n production
./drain_node.sh node-1 5m
```

Usa `maxUnavailable: 1` como default; cambia a `minAvailable` solo cuando un servicio necesite un piso garantizado (StatefulSets con quorum). Nunca pongas `minAvailable` igual al número de réplicas — todos los drains se quedarán colgados.
