# GitOps en Producción — Companion

Manifiestos de Kubernetes y config de pipeline para la guía de StackPractices
[Guía Completa de GitOps en Producción](https://stackpractices.com/es/guides/complete-guide-gitops-production/).

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `argocd/application.yaml` | Application de ArgoCD con sync automatizado, prune, self-heal y retry |
| `argocd/appproject-production.yaml` | AppProject con listas de repos/destinos permitidos, whitelist/blacklist de recursos y RBAC por equipo |
| `argocd/applicationset-multi-cluster.yaml` | ApplicationSet que genera un Application por cluster de producción |
| `flux/gitrepository.yaml` | Source GitRepository con referencia a deploy-key |
| `flux/kustomization.yaml` | Kustomization con prune, wait, health checks y sustitución post-build |
| `flux/kustomization-sops.yaml` | Kustomization con descifrado SOPS/age |
| `flux/helmrelease-redis.yaml` | HelmRelease fijado a un rango de versión mayor del chart |
| `progressive-delivery/rollout-canary.yaml` | Canary de Argo Rollouts con traffic routing nginx y análisis |
| `progressive-delivery/analysis-template.yaml` | AnalysisTemplate basado en Prometheus (gate de tasa de éxito) |
| `progressive-delivery/flagger-canary.yaml` | Canary de Flagger con checks de métricas y webhook de load-test |
| `secrets/api-secrets.sops.yaml` | Ejemplo de Secret cifrado con SOPS (age) |
| `ci/deploy-workflow.yaml` | Workflow de GitHub Actions que construye la imagen y actualiza el repo GitOps |

## Inicio rápido

```bash
# ArgoCD
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
kubectl apply -f argocd/

# Flux
flux bootstrap github --owner=myorg --repository=fleet-infra \
  --branch=main --path=clusters/production --personal=false
kubectl apply -f flux/
```

Adaptá `repoURL`, las URLs de los clusters, los namespaces y las referencias a secretos a tu entorno antes de aplicar.
