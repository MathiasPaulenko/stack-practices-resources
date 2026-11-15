# ConfigMap & Secret Mounting — Companion Manifests

Runnable manifests for the StackPractices recipe
[Mount Configs and Secrets into Kubernetes Pods](https://stackpractices.com/recipes/kubernetes-configmap-secret-mounting/).

Each file maps to an injection pattern from the recipe. Apply the shared sources
(`configmap.yaml`, `secret.yaml`) first, then whichever deployment shows the
pattern you want to test.

## Files

| File | What it shows |
|------|---------------|
| `configmap.yaml` | ConfigMap with literal keys plus an embedded `config.yaml` |
| `secret.yaml` | Opaque Secret using `stringData` (plain-text input, base64-encoded on write) |
| `configmap-immutable.yaml` | `immutable: true` — kubelet stops watching, edits are rejected |
| `configmap-template.yaml` | `config.yaml.tpl` template consumed by the init-container example |
| `deployment-env-vars.yaml` | `envFrom` bulk load + individual `secretKeyRef` entries |
| `deployment-envfrom-prefix.yaml` | `envFrom` with `APP_`/`SECRET_` prefixes to avoid key collisions |
| `deployment-env-selective.yaml` | `configMapKeyRef`/`secretKeyRef` for single keys, `optional: false` |
| `deployment-config-volume.yaml` | ConfigMap as a volume with `items` key→file mapping |
| `deployment-secret-volume.yaml` | Secret volume with `defaultMode: 0400` |
| `deployment-projected.yaml` | Projected volume merging ConfigMap + Secret into one mount |
| `deployment-subpath.yaml` | `subPath` single-file mount (no live updates — static at start) |
| `tls-secret.yaml` | `kubernetes.io/tls` Secret with a self-signed demo cert |
| `deployment-tls-volume.yaml` | Mounting `tls.crt`/`tls.key` at `/etc/tls` |
| `deployment-image-pull-secret.yaml` | `dockerconfigjson` Secret + `imagePullSecrets` for a private registry |
| `deployment-init-container.yaml` | Init container rendering a template into a shared `emptyDir` |
| `externalsecret.yaml` | External Secrets Operator sync from AWS Secrets Manager |
| `sealedsecret.yaml` | Bitnami SealedSecret placeholder (encrypt with `kubeseal` first) |

## Try it

```bash
# Base objects required by most deployments
kubectl apply -f configmap.yaml -f secret.yaml

# Pick an injection pattern
kubectl apply -f deployment-config-volume.yaml

# Verify what the pod actually received
kubectl exec deploy/my-app -- env | grep DATABASE
kubectl exec deploy/my-app -- ls -l /etc/app/config
```

## Notes

- `tls-secret.yaml` ships a self-signed cert for `demo.internal` — replace it
  with a real certificate (`kubectl create secret tls tls-secret --cert=... --key=...`).
- `externalsecret.yaml` needs the External Secrets Operator CRDs and a
  `ClusterSecretStore` named `aws-secrets-manager`.
- `sealedsecret.yaml` is a template: run `kubeseal --format yaml < secret.yaml`
  to produce real `encryptedData` for your cluster.
- `deployment-image-pull-secret.yaml` uses a fake registry credential — the
  Secret applies fine, but the pull will fail against `private-registry.io`
  unless you point it at a registry you control.
