# Kubernetes Advanced Guide — Companion Manifests

Apply-ready manifests for the [Kubernetes Advanced guide](https://stackpractices.com/guides/kubernetes-advanced-guide/) on StackPractices.

## Contents

| File | What it does |
|---|---|
| `crd-database.yaml` | `CustomResourceDefinition` with `openAPIV3Schema` validation for a `Database` kind |
| `namespace-restricted.yaml` | Namespace enforcing the `restricted` Pod Security Standard (enforce + warn + audit) |
| `secure-pod.yaml` | Pod that satisfies `restricted` PSS — non-root, read-only rootfs, dropped capabilities, resource limits |
| `network-policy.yaml` | Selective allow policy for a `frontend` tier (ingress from ingress-nginx, egress to backend + DNS) |
| `rbac-ci.yaml` | Least-privilege `Role` + `RoleBinding` for a CI `ServiceAccount` |
| `applicationset.yaml` | ArgoCD `ApplicationSet` that rolls the same app out to every registered cluster |

## Usage

Try it on a local cluster (kind, minikube, Docker Desktop):

```bash
kubectl create namespace demo
kubectl apply -f namespace-restricted.yaml
kubectl apply -f secure-pod.yaml -n production
kubectl apply -f network-policy.yaml -n <ns>
kubectl apply -f rbac-ci.yaml -n <ns>
kubectl apply -f crd-database.yaml   # cluster-scoped
kubectl get crd databases.mycompany.com
```

`applicationset.yaml` requires an ArgoCD installation; it targets `argoproj.io/v1alpha1` and generates one `Application` per registered cluster.

## Notes

- `secure-pod.yaml` mounts an `emptyDir` at `/tmp` because `readOnlyRootFilesystem` blocks writes — adjust paths to your image.
- NetworkPolicy only works if your CNI enforces it (Calico and Cilium do; many managed CNIs don't by default).
- These are teaching manifests — review labels, namespaces, and image tags before using them anywhere real.
