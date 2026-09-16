# Deployment Rollback — Companion Resources

Companion files for the [Deployment Rollback Runbook](https://stackpractices.com/docs/deployment-rollback-runbook/) on StackPractices.com.

## What's included

| File | Format | Description |
|------|--------|-------------|
| `rollback-runbook.md` | Markdown | Ready-to-adapt runbook: triggers, verification checklist, and communication template |
| `rollback-commands.sh` | Bash | Function library for kubectl/Helm/ArgoCD rollback with `APP`/`NS` env vars |

## Quick start

### 1. Copy the runbook

```bash
cp rollback-runbook.md oncall/rollback-runbook.md
```

Fill in your app name, namespace, thresholds, and stakeholder channels.

### 2. Use the command library

```bash
source rollback-commands.sh
export APP=my-app NS=production

rollback_kubectl          # undo to previous revision
rollback_kubectl_to 3     # undo to a specific revision
rollback_helm             # helm rollback to previous revision
verify_rollback           # image + pods + logs + events
argocd_git_revert <sha>   # GitOps revert — persists in Git (unlike `argocd app rollback`)
```

## Trigger thresholds (defaults from the runbook)

| Trigger | Severity | Action | Timeline |
|---------|----------|--------|----------|
| Error rate > 5% | Critical | Rollback immediately | < 5 min |
| P99 latency > 5x baseline | Critical | Rollback immediately | < 5 min |
| Health check failures | Critical | Rollback immediately | < 5 min |
| Error rate > 1% | High | Investigate, prepare | < 15 min |
| OOM kills increasing | High | Rollback if trending | < 10 min |

## References

- [Kubernetes Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [Helm rollback](https://helm.sh/docs/helm/helm_rollback/)
- [Argo CD documentation](https://argo-cd.readthedocs.io/)
