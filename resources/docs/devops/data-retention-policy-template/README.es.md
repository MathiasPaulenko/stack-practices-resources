# Plantilla de Política de Retención de Datos — Companion

Plantilla rellenable de política de retención con implementaciones ejecutables:

- `retention-policy-template.md` — plantilla para rellenar (alcance/roles, tabla de retención, reglas por clasificación, checklist de eliminación).
- `s3-lifecycle.json` — reglas de ciclo de vida S3: transición de logs a Glacier/Deep Archive, expiración de datos temporales, expiración de versiones de datos de usuario.
- `purge.sql` — job programado de purga en PostgreSQL (sesiones, datos de usuarios eliminados, logs de eventos) con VACUUM.

Fuente: https://stackpractices.com/es/docs/data-retention-policy-template/

Adaptá cada período de retención a tu base legal antes de aplicarlo — los ejemplos son ilustrativos, no asesoría legal.
