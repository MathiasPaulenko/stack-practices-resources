# Kubernetes Config Management — Companion

Runnable manifests for the StackPractices guide
[Kubernetes Config Management Guide](https://stackpractices.com/guides/complete-guide-kubernetes-config-management/).

- `manifests/configmap.yaml` — immutable ConfigMap with env + file keys
- `manifests/secret.yaml` — Secret via `stringData`
- `manifests/deployment.yaml` — envFrom + volume mount + Reloader annotations
- `manifests/externalsecret.yaml` — ESO ExternalSecret pointing at a Vault SecretStore
- `manifests/rbac.yaml` — Role/RoleBinding scoped to one secret
- `scripts/kind-setup.sh` — creates a kind cluster and applies everything

## Run

```bash
./scripts/kind-setup.sh
kubectl -n production describe deploy app
```
