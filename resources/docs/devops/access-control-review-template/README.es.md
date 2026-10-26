# Plantilla de Revisión de Control de Acceso — Recursos complementarios

Archivos complementarios de la [Plantilla de Revisión de Control de Acceso](https://stackpractices.com/es/docs/access-control-review-template/) en StackPractices.

## Contenido

| Archivo | Propósito |
|---------|-----------|
| `aws-iam-access-analyzer.sh` | Lista usuarios IAM con última actividad, marca access keys sin uso y exporta hallazgos activos de IAM Access Analyzer (define `ANALYZER_ARN` para activarlo) |
| `github-org-access-audit.py` | Lista miembros de una org de GitHub y marca cuentas inactivas más de 90 días vía la API de eventos públicos |
| `k8s-rbac-audit.sh` | Audita bindings de cluster-admin, RoleBindings por namespace y service accounts que aún referencian secrets |

## Uso

```bash
# Snapshot de AWS IAM
aws sts get-caller-identity   # verifica credenciales primero
./aws-iam-access-analyzer.sh

# Auditoría de org de GitHub
pip install requests
python github-org-access-audit.py <github-token>

# Auditoría RBAC de Kubernetes
kubectl config current-context  # verifica el contexto primero
./k8s-rbac-audit.sh
```

Vuelca la salida de estos scripts en el registro de accesos de la plantilla de revisión — cada hallazgo se convierte en una fila con veredicto (mantener / modificar / retirar) y un motivo.
