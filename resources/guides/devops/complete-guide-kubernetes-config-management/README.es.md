# Gestión de Configuración en Kubernetes — Companion

Manifiestos ejecutables de la guía de StackPractices
[Guía de Gestión de Configuración en Kubernetes](https://stackpractices.com/es/guides/complete-guide-kubernetes-config-management/).

- `manifests/configmap.yaml` — ConfigMap inmutable con keys env + archivo
- `manifests/secret.yaml` — Secret vía `stringData`
- `manifests/deployment.yaml` — envFrom + mount de volumen + anotaciones de Reloader
- `manifests/externalsecret.yaml` — ExternalSecret de ESO apuntando a un SecretStore de Vault
- `manifests/rbac.yaml` — Role/RoleBinding acotado a un solo secret
- `scripts/kind-setup.sh` — crea un cluster kind y aplica todo

## Ejecutar

```bash
./scripts/kind-setup.sh
kubectl -n production describe deploy app
```
