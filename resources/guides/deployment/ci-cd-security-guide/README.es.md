# Recursos de la Guía de Seguridad CI/CD

Recursos complementarios de [Seguridad en Pipelines CI/CD: Prevén Ataques a la Cadena de Suministro](https://stackpractices.com/es/guides/ci-cd-security-guide/).

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `ci/secure-workflow.yml` | Workflow endurecido de GitHub Actions: actions fijadas por SHA, permisos mínimos, auth OIDC, escaneo Trivy, firma cosign, aprobación manual a producción |
| `ci/runner-hardening-checklist.md` | Checklist de seguridad para runners auto-hospedados: aislamiento, builds rootless, runners efímeros, logging de auditoría |

## Uso

1. Copia `ci/secure-workflow.yml` a `.github/workflows/` y ajusta el ARN del rol, la región y el nombre de imagen.
2. Revisa `ci/runner-hardening-checklist.md` para cualquier runner auto-hospedado.
