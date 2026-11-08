# Data Privacy and GDPR Compliance — Companion Examples

Runnable technical controls referenced by the recipe
[Data Privacy and GDPR Compliance](https://stackpractices.com/recipes/data-privacy-gdpr/).

## Files

| File | What it does |
|------|--------------|
| `schema.sql` | PostgreSQL consent table with per-purpose grant/withdrawal audit fields |
| `pseudonymize.py` | HMAC-SHA256 pseudonymization + age bucketing for analytics |
| `consent_api.js` | Express router: grant, withdraw, and list consents |
| `export_user_data.py` | GDPR Art. 20 portability export — ZIP with JSON per data section |
| `retention_cleanup.py` | Cron job that deletes/anonymizes records past retention policies |

## Usage

```bash
# Pseudonymization (needs a key — use a real one from your secrets manager)
export PII_HMAC_KEY="your-secret-key"
python pseudonymize.py
```

`consent_api.js` expects `db` and `eventBus` adapters from your stack
(ORM client and event publisher); wire the router with `app.use(router)`.

## Notes

- Never hardcode the HMAC key — the file reads `PII_HMAC_KEY` from the
  environment and falls back to a dev-only value with a warning path.
- Pseudonymized data remains personal data under GDPR. Only irreversible
  anonymization falls outside the regulation.
