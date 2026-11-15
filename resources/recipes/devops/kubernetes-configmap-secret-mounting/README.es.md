# Montaje de ConfigMaps y Secrets — Manifiestos complementarios

Manifiestos ejecutables de la receta de StackPractices
[Montar ConfigMaps y Secrets en Pods de Kubernetes](https://stackpractices.com/es/recipes/kubernetes-configmap-secret-mounting/).

Cada archivo corresponde a un patrón de inyección de la receta. Aplica primero
las fuentes compartidas (`configmap.yaml`, `secret.yaml`) y después el
deployment del patrón que quieras probar.

## Archivos

| Archivo | Qué muestra |
|---------|-------------|
| `configmap.yaml` | ConfigMap con claves literales más un `config.yaml` embebido |
| `secret.yaml` | Secret Opaque con `stringData` (entrada en texto plano, se codifica al escribir) |
| `configmap-immutable.yaml` | `immutable: true` — el kubelet deja de vigilarlo, las ediciones se rechazan |
| `configmap-template.yaml` | Template `config.yaml.tpl` consumido por el ejemplo de init container |
| `deployment-env-vars.yaml` | Carga masiva con `envFrom` + entradas individuales con `secretKeyRef` |
| `deployment-envfrom-prefix.yaml` | `envFrom` con prefijos `APP_`/`SECRET_` para evitar colisiones de claves |
| `deployment-env-selective.yaml` | `configMapKeyRef`/`secretKeyRef` para claves sueltas, `optional: false` |
| `deployment-config-volume.yaml` | ConfigMap como volumen con mapeo `items` clave→archivo |
| `deployment-secret-volume.yaml` | Volumen de Secret con `defaultMode: 0400` |
| `deployment-projected.yaml` | Volumen proyectado que fusiona ConfigMap + Secret en un solo montaje |
| `deployment-subpath.yaml` | Montaje de un solo archivo con `subPath` (sin actualizaciones en vivo) |
| `tls-secret.yaml` | Secret `kubernetes.io/tls` con un cert demo autofirmado |
| `deployment-tls-volume.yaml` | Montaje de `tls.crt`/`tls.key` en `/etc/tls` |
| `deployment-image-pull-secret.yaml` | Secret `dockerconfigjson` + `imagePullSecrets` para registro privado |
| `deployment-init-container.yaml` | Init container que renderiza un template en un `emptyDir` compartido |
| `externalsecret.yaml` | Sincronización con External Secrets Operator desde AWS Secrets Manager |
| `sealedsecret.yaml` | Plantilla de SealedSecret de Bitnami (cifra con `kubeseal` primero) |

## Pruébalo

```bash
# Objetos base que necesitan la mayoría de los deployments
kubectl apply -f configmap.yaml -f secret.yaml

# Elige un patrón de inyección
kubectl apply -f deployment-config-volume.yaml

# Verifica qué recibió realmente el pod
kubectl exec deploy/my-app -- env | grep DATABASE
kubectl exec deploy/my-app -- ls -l /etc/app/config
```

## Notas

- `tls-secret.yaml` trae un cert autofirmado para `demo.internal` — reemplázalo
  por un certificado real (`kubectl create secret tls tls-secret --cert=... --key=...`).
- `externalsecret.yaml` necesita los CRD de External Secrets Operator y un
  `ClusterSecretStore` llamado `aws-secrets-manager`.
- `sealedsecret.yaml` es una plantilla: ejecuta `kubeseal --format yaml < secret.yaml`
  para generar el `encryptedData` real de tu clúster.
- `deployment-image-pull-secret.yaml` usa una credencial de registro falsa — el
  Secret se aplica sin problema, pero el pull fallará contra `private-registry.io`
  salvo que apuntes a un registro que controles.
