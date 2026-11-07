# Checklist de Auditoría de Core Web Vitals — Archivos complementarios

Artefactos descargables del [Checklist de Auditoría de Core Web Vitals](https://stackpractices.com/es/docs/core-web-vitals-audit-checklist/) en StackPractices.

## Archivos

| Archivo | Qué es |
|---|---|
| `cwv-issue-tracker.csv` | Tracker de issues con filas de ejemplo — impórtalo en Sheets/Jira y reemplázalo con tus hallazgos |
| `audit-report-template.md` | Informe de auditoría en blanco (campo + lab + hallazgos + plan de remediación) listo para rellenar |
| `web-vitals-rum.js` | Snippet de recolección RUM con la librería `web-vitals` — envía LCP/INP/CLS a tu endpoint |

## Uso

1. Ejecuta el checklist en tus tipos de página (herramientas: Lighthouse, PSI, CrUX, WebPageTest).
2. Registra los hallazgos en `cwv-issue-tracker.csv` con responsable y objetivo.
3. Rellena `audit-report-template.md` por cada página auditada.
4. Añade `web-vitals-rum.js` al entry point de tu app para empezar a recoger datos de campo.

Objetivos en P75 móvil: **LCP ≤ 2,5s · INP ≤ 200ms · CLS ≤ 0,1**

## Relacionados

- Doc: https://stackpractices.com/es/docs/core-web-vitals-audit-checklist/
- Referencia Web Vitals: https://web.dev/vitals/
