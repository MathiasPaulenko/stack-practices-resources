# Plantilla de Política RBAC — Recursos Companion

Artefactos descargables para el documento [Plantilla de Política RBAC](https://stackpractices.com/es/docs/rbac-policy-template/) de StackPractices.

## Archivos

| Archivo | Qué es |
|---------|--------|
| `rbac-policy-template.md` | La plantilla completa del documento de política — matriz de roles, reglas de asignación, separación de deberes, flujo de solicitud, cadencia de revisión, baja de personal, break-glass y excepciones. Rellena los marcadores entre corchetes. |
| `kubernetes-rbac.yaml` | `Role` + `RoleBinding` de Kubernetes (developers de solo lectura) y un `ClusterRole` para el equipo de plataforma que gestiona objetos RBAC. Aplica con `kubectl apply -f kubernetes-rbac.yaml`. |
| `aws-iam-boundary-policy.json` | Política AWS IAM con acceso S3 de privilegio mínimo, denegación estricta de borrado de buckets y requisito de MFA para acciones IAM sensibles. |
| `opa-prevent-privilege-escalation.yaml` | Constraint de OPA Gatekeeper que bloquea bindings a `cluster-admin` fuera de los equipos de plataforma y seguridad. |
| `opa-rolebinding-validation.rego` | La regla Rego detrás de la constraint — valida role bindings contra una lista de roles prohibidos. |

## Cómo usarlo

1. Copia `rbac-policy-template.md` en tu repositorio de políticas y reemplaza los marcadores entre corchetes.
2. Mapea cada fila de rol a un grupo en tu proveedor de identidad o a un binding en Kubernetes/IAM de nube.
3. Adapta el manifiesto y las políticas a tus namespaces, grupos y nombres de bucket.
4. Guarda todo bajo control de versiones — los cambios de política pasan por la misma revisión que el código.

## Relacionados

- Documento: https://stackpractices.com/es/docs/rbac-policy-template/
- Receta: https://stackpractices.com/es/recipes/implement-rbac/
- Documento (EN): https://stackpractices.com/docs/rbac-policy-template/
