# GitOps in Production — Companion

Kubernetes manifests and pipeline config for the StackPractices guide
[Complete Guide to GitOps in Production](https://stackpractices.com/guides/complete-guide-gitops-production/).

## Files

| File | Description |
|------|-------------|
| `argocd/application.yaml` | ArgoCD Application with automated sync, prune, self-heal and retry |
| `argocd/appproject-production.yaml` | AppProject with repo/destination allow-lists, resource whitelist/blacklist and team RBAC |
| `argocd/applicationset-multi-cluster.yaml` | ApplicationSet generating one Application per prod cluster |
| `flux/gitrepository.yaml` | GitRepository source with deploy-key reference |
| `flux/kustomization.yaml` | Kustomization with prune, wait, health checks and post-build substitution |
| `flux/kustomization-sops.yaml` | Kustomization with SOPS/age decryption |
| `flux/helmrelease-redis.yaml` | HelmRelease pinned to a major-version chart range |
| `progressive-delivery/rollout-canary.yaml` | Argo Rollouts canary with nginx traffic routing and analysis |
| `progressive-delivery/analysis-template.yaml` | Prometheus-based AnalysisTemplate (success-rate gate) |
| `progressive-delivery/flagger-canary.yaml` | Flagger Canary with metric checks and load-test webhook |
| `secrets/api-secrets.sops.yaml` | Example SOPS-encrypted Secret (age) |
| `ci/deploy-workflow.yaml` | GitHub Actions workflow that builds the image and updates the GitOps repo |

## Quick start

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

Adapt `repoURL`, cluster URLs, namespaces and secret references to your environment before applying.
