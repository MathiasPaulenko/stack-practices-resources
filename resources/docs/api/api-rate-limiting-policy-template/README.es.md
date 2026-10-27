# Plantilla de Política de Rate Limiting — Recursos Complementarios

Archivos complementarios de la [Plantilla de Política de Rate Limiting](https://stackpractices.com/es/docs/api-rate-limiting-policy-template/).

| Archivo | Qué muestra |
|---------|-------------|
| `rate-limiting-policy-template.md` | El documento de política para rellenar (tiers, alcances, headers, escalado) |
| `express_rate_limit.js` | Token bucket en Redis + middleware Express con headers 429 |
| `python_rate_limit.py` | Token bucket en Redis con Python |
| `retry_client.js` | Reintento del lado del cliente respetando `Retry-After` con jitter |
