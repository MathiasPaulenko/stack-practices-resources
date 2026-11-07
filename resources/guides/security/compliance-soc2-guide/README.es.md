# Guía de Cumplimiento SOC 2 — Compañero

Artefactos de evidencia para los controles de la guía:

- `soc2-evidence-map.md` — mapeo control → evidencia → automatización para las nueve familias de Criterios Comunes.
- `access_review_diff.py` — compara dos exportaciones trimestrales del IAM (CSV) y reporta altas, bajas y cambios de rol. El diff más el ticket de revisión es tu evidencia de CC6.
- `pr_approval_export.py` — exporta los revisores de PRs fusionados vía la API REST de GitHub a un CSV de auditoría para CC8.
- `vendor-due-diligence-checklist.md` — lista repetible de alta/revisión de proveedores para CC9 y el seguimiento de organizaciones de subservicio.

## Uso

1. Apunta `access_review_diff.py` a las exportaciones del IAM de este trimestre y el anterior: `python access_review_diff.py q1.csv q2.csv`.
2. Define `GITHUB_TOKEN` y ejecuta `pr_approval_export.py` cada mes para archivar el rastro de aprobaciones.
3. Guarda un `vendor-due-diligence-checklist.md` completado por organización de subservicio, con revisión anual.

Artículo fuente: <https://stackpractices.com/es/guides/compliance-soc2-guide/>
