# Complete Guide to GitOps with ArgoCD — Companion Assets

ArgoCD manifests from the
[Complete Guide to GitOps with ArgoCD](https://stackpractices.com/guides/complete-guide-gitops-argocd/).

## Contents

| File | What it shows |
| --- | --- |
| `application.yaml` | Basic Application with automated sync + selfHeal |
| `applicationset-multi-env.yaml` | ApplicationSet with list generator (dev/staging/prod) |
| `appproject-rbac.yaml` | AppProject with sourceRepos/destinations/syncWindows + Casbin RBAC ConfigMap |
| `notifications-cm.yaml` | Slack notifications: triggers + templates |
| `sync-windows.yaml` | Deny/allow sync windows for a project |

## Usage

```bash
kubectl apply -f appproject-rbac.yaml   # project + RBAC first
kubectl apply -f applicationset-multi-env.yaml
```
