# OWASP Top 10 2025 — Checklist de remediación

Archivos complementarios de la [Checklist de remediación OWASP Top 10 2025](https://stackpractices.com/es/docs/owasp-top-10-remediation-checklist/) en StackPractices.

## Contenido

- `owasp-top-10-2025-remediation-checklist.md` — las diez categorías en tablas imprimibles, ordenadas por prioridad (P0 primero). Cópialas en tu gestor de issues o espacio de auditoría.
- `remediation-tracker.csv` — tracker inicial con una fila por check P0. Columnas: `category`, `check`, `priority`, `status`, `owner`, `evidence`, `revisit_date`, `retest_result`. Extiéndelo con los ítems P1/P2 de la checklist completa.
- `owasp-top-10-2025-remediation-checklist.es.md` — versión en español de la checklist.

## Uso

1. Importa el CSV en Jira, Linear, GitHub Issues o una hoja de cálculo.
2. Recorre cada categoría de arriba hacia abajo; marca `status` como `open / in progress / verified / accepted-risk`.
3. Registra la prueba en `evidence`: el commit, la prueba de regresión o la salida del escáner que demuestra que la corrección funciona.
4. Repite la sección afectada tras hallazgos de pentest; haz la pasada completa cada trimestre.

Para el código de mitigación ejecutable (protección SSRF, control de acceso, manejo fail-closed, tests de pytest), mira el recurso hermano `resources/guides/security/complete-guide-owasp-top-10-2025/`.
