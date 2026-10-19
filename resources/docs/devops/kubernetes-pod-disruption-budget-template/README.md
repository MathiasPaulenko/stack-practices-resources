# Kubernetes Pod Disruption Budget Template

Companion resources for the [Kubernetes Pod Disruption Budget Template](https://stackpractices.com/docs/kubernetes-pod-disruption-budget-template/) on StackPractices.

## Files

| File | What it covers |
|------|----------------|
| `pdb_minavailable.yaml` | Standard PDB with a fixed `minAvailable` floor |
| `pdb_maxunavailable.yaml` | PDB with `maxUnavailable: 1` — the sanest default for most services |
| `pdb_percentage.yaml` | Percentage-based PDB that scales with replica count (HPA-friendly) |
| `pdb_statefulset.yaml` | Quorum-aware PDB for StatefulSets (databases, etcd) |
| `helm_pdb_template.yaml` | PDB block to drop into a Helm chart `templates/` directory |
| `prometheus_pdb_alerts.yaml` | Prometheus rules for blocked drains and unhealthy budgets |
| `drain_node.sh` | Node drain script that surfaces blocking PDBs before draining |

## Usage

Apply a PDB before draining any node:

```bash
kubectl apply -f pdb_maxunavailable.yaml
kubectl get pdb -n production
./drain_node.sh node-1 5m
```

Use `maxUnavailable: 1` as the default; switch to `minAvailable` only when a service needs a guaranteed floor (quorum-based StatefulSets). Never set `minAvailable` equal to the replica count — every drain will hang.
