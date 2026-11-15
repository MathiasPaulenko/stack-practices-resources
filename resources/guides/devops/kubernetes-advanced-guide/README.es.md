# Guía Avanzada de Kubernetes — Manifiestos Companion

Manifiestos listos para aplicar de la [guía avanzada de Kubernetes](https://stackpractices.com/es/guides/kubernetes-advanced-guide/) en StackPractices.

## Contenido

| Archivo | Qué hace |
|---|---|
| `crd-database.yaml` | `CustomResourceDefinition` con validación `openAPIV3Schema` para un kind `Database` |
| `namespace-restricted.yaml` | Namespace que aplica el Pod Security Standard `restricted` (enforce + warn + audit) |
| `secure-pod.yaml` | Pod que satisface `restricted` PSS — no-root, rootfs de solo lectura, capabilities eliminadas, límites de recursos |
| `network-policy.yaml` | Política de allowlist para un tier `frontend` (ingress desde ingress-nginx, egress a backend + DNS) |
| `rbac-ci.yaml` | `Role` + `RoleBinding` de mínimo privilegio para un `ServiceAccount` de CI |
| `applicationset.yaml` | `ApplicationSet` de ArgoCD que despliega la misma app en cada cluster registrado |

## Uso

Pruébalo en un cluster local (kind, minikube, Docker Desktop):

```bash
kubectl create namespace demo
kubectl apply -f namespace-restricted.yaml
kubectl apply -f secure-pod.yaml -n production
kubectl apply -f network-policy.yaml -n <ns>
kubectl apply -f rbac-ci.yaml -n <ns>
kubectl apply -f crd-database.yaml   # cluster-scoped
kubectl get crd databases.mycompany.com
```

`applicationset.yaml` requiere una instalación de ArgoCD; apunta a `argoproj.io/v1alpha1` y genera una `Application` por cluster registrado.

## Notas

- `secure-pod.yaml` monta un `emptyDir` en `/tmp` porque `readOnlyRootFilesystem` bloquea escrituras — ajusta las rutas a tu imagen.
- NetworkPolicy solo funciona si tu CNI la aplica (Calico y Cilium lo hacen; muchos CNIs gestionados no por defecto).
- Son manifiestos didácticos — revisa labels, namespaces y tags de imagen antes de usarlos en algo real.
