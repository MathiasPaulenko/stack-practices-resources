# security-review-checklist-for-prs

Recursos complementarios para la guía [Checklist de Revisión de Seguridad para PRs](https://stackpractices.com/es/docs/security-review-checklist-for-prs/) en StackPractices.com.

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `pre-commit-config.yaml` | Hooks pre-commit para GitLeaks y detect-secrets |
| `semgrep.yml` | Reglas de seguridad personalizadas de Semgrep para revisión de PRs |
| `security-review.yml` | Workflow de GitHub Actions para verificaciones de seguridad automatizadas |

## Uso

1. Copia `pre-commit-config.yaml` a la raíz de tu repo y ejecuta `pre-commit install`.
2. Copia `semgrep.yml` a la raíz de tu repo y ejecuta `semgrep --config semgrep.yml`.
3. Copia `security-review.yml` a `.github/workflows/` y configura el secret `SNYK_TOKEN`.

## Requisitos

- [pre-commit](https://pre-commit.com/) >= 3.0
- [Semgrep](https://semgrep.dev/) >= 1.0
- [Snyk CLI](https://snyk.io/) (opcional, para escaneo de dependencias)
- [GitLeaks](https://github.com/gitleaks/gitleaks) >= 8.0
