# Guía Completa de Gestión de Secretos — Scripts compañeros

Compañero de [Guía Completa de Gestión de Secretos](https://stackpractices.com/es/guides/complete-guide-secrets-management/).

- `rotate_secret.sh` — rotación sin downtime: guardar nueva versión, despliegue rodante, promover, deprecar la vieja.
- `scan_secrets.sh` — escaneo de historial con gitleaks para local y CI.
- `external-secret.yaml` — External Secrets Operator sincronizando AWS Secrets Manager a Kubernetes.

Recuerda: ante un acierto del escáner, rota primero —borrar la línea no quita el secreto del historial.
