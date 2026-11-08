# Privacidad de Datos y Cumplimiento GDPR — Ejemplos Companion

Controles técnicos ejecutables referenciados por la receta
[Privacidad de Datos y Cumplimiento GDPR](https://stackpractices.com/es/recipes/data-privacy-gdpr/).

## Archivos

| Archivo | Qué hace |
|---------|----------|
| `schema.sql` | Tabla de consentimientos PostgreSQL con campos de auditoría por propósito |
| `pseudonymize.py` | Seudonimización HMAC-SHA256 + rangos de edad para analítica |
| `consent_api.js` | Router Express: otorgar, retirar y listar consentimientos |
| `export_user_data.py` | Exportación de portabilidad Art. 20 — ZIP con JSON por sección |
| `retention_cleanup.py` | Job cron que borra/anonimiza registros vencidos por retención |

## Uso

```bash
# Seudonimización (necesita clave — usa una real de tu gestor de secretos)
export PII_HMAC_KEY="your-secret-key"
python pseudonymize.py
```

`consent_api.js` espera adaptadores `db` y `eventBus` de tu stack
(cliente ORM y publicador de eventos); monta el router con `app.use(router)`.

## Notas

- Nunca hardcodees la clave HMAC — el archivo lee `PII_HMAC_KEY` del entorno
  y usa un valor de desarrollo solo como fallback.
- El dato seudonimizado sigue siendo dato personal bajo GDPR. Solo la
  anonimización irreversible queda fuera del reglamento.
