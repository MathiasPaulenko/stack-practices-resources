# Plantilla de Checklist para Code Review — Archivos Companion

Companion de la plantilla de StackPractices [Plantilla de Checklist para Code Review](https://stackpractices.com/es/docs/code-review-checklist-template/).

| Archivo | Contiene |
|---|---|
| src/code-review-checklist.md | Checklist en markdown lista para copiar: 7 dimensiones, tabla de notas de revisión, veredicto y confirmación del revisor |
| src/code-review-automation.yml | Workflow de GitHub Actions: análisis CodeQL, gate de lint/typecheck y aviso de PRs demasiado grandes |
| src/pr-checklist-validator.py | Bot en Python que verifica tests añadidos, ausencia de secretos en el diff y descripción de PR completa |
| src/review-metrics.py | Script de métricas de revisión: tiempo de ciclo, comentarios por PR, tasa de escape de defectos y estadísticas por revisor |

## Uso

- Pegá `code-review-checklist.md` en tu wiki o en `.github/pull_request_template.md`.
- Copiá `code-review-automation.yml` a `.github/workflows/` y ajustá la lista de `languages` de CodeQL a tu stack.
- Ejecutá `python src/pr-checklist-validator.py` dentro de una rama de PR (espera `origin/main` como base).
- Alimentá `review-metrics.py` con los metadatos de tus PRs para medir la salud de las revisiones del equipo.
