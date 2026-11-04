# Guía Completa de GitOps con ArgoCD — Assets del ejemplo

Manifiestos de ArgoCD de la
[Guía Completa de GitOps con ArgoCD](https://stackpractices.com/es/guides/complete-guide-gitops-argocd/).

## Contenido

| Archivo | Qué muestra |
| --- | --- |
| `application.yaml` | Application básica con sync automatizado + selfHeal |
| `applicationset-multi-env.yaml` | ApplicationSet con generador list (dev/staging/prod) |
| `appproject-rbac.yaml` | AppProject con sourceRepos/destinations/syncWindows + ConfigMap Casbin RBAC |
| `notifications-cm.yaml` | Notificaciones Slack: triggers + templates |
| `sync-windows.yaml` | Ventanas de sync deny/allow para un proyecto |

## Uso

```bash
kubectl apply -f appproject-rbac.yaml   # proyecto + RBAC primero
kubectl apply -f applicationset-multi-env.yaml
```
