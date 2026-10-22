# Plantilla de Revisión de Seguridad de API — Recursos complementarios

Checklist rellenable de revisión de seguridad de API mapeado al OWASP API Security Top 10 (2023), más un ejemplo completo.

## Archivos

- `api-security-review-template.md` — el checklist en blanco: metadatos, autenticación, autorización, validación de entrada, tiers de rate limiting, gestión de secretos, protección de datos, manejo de errores y logging, tabla de cobertura OWASP API Top 10 y sección de hallazgos/cierre.
- `example-filled.md` — la misma plantilla completada para una API REST pública ficticia (`payments-api`), mostrando cómo las casillas sin marcar se convierten en una tabla de hallazgos con severidad, responsable y fecha límite.

## Cómo usarla

1. Copia `api-security-review-template.md` a tu repo, wiki o un ticket.
2. Rellena los metadatos y trabaja cada sección para una API (o un grupo de endpoints).
3. Mueve cada casilla sin marcar a la tabla de hallazgos con severidad, responsable y fecha límite.
4. Archiva la revisión completada — los auditores piden evidencia, no intenciones.

Fuente: [Plantilla de Revisión de Seguridad de API](https://stackpractices.com/es/docs/api-security-review-template/)
