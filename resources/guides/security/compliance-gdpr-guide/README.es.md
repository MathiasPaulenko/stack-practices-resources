# Guía de Cumplimiento GDPR — Compañero

Esquema SQL para las tablas de consentimiento y DSAR de la guía:

- `consent_schema.sql` — `user_consents` (por finalidad, versionado, con retirada) y `dsar_requests` (tipo, estado, tracking del SLA), más el cron de auto-borrado de cuentas inactivas.

## Uso

1. Ejecuta el esquema contra tu Postgres (adapta tipos para MySQL/SQLite).
2. Registra cada concesión/retirada de consentimiento — un booleano desnudo no basta ante un auditor.
3. Conecta la entrada de DSAR a un canal de tickets; el reloj de 30 días arranca en la recepción.

Artículo fuente: <https://stackpractices.com/es/guides/compliance-gdpr-guide/>
