# Estrategias de invalidación de caché CDN — Archivos complementarios

Código ejecutable que acompaña a la receta de StackPractices
[Estrategias y patrones de invalidación de caché CDN](https://stackpractices.com/es/recipes/cdn-cache-invalidation-strategies/).

## Archivos

- `cdn_invalidate.py` — helpers de purge para Cloudflare (URLs, cache tags, purge total), Fastly (URLs, surrogate keys, soft purge) y AWS CloudFront (invalidaciones por path), además de un hook de despliegue controlado por `CDN_PROVIDER`.
- `webhook_server.py` — endpoint FastAPI que recibe eventos de CMS (`product_updated`, `full_deploy`) y ejecuta el purge correspondiente. Requiere `WEBHOOK_SECRET` y las credenciales del proveedor.

## Uso

```bash
pip install httpx boto3 fastapi uvicorn

# Purgar todo al desplegar
export CDN_PROVIDER=cloudflare
export CLOUDFLARE_ZONE_ID=... CLOUDFLARE_API_TOKEN=...
python cdn_invalidate.py

# O levantar el webhook para purges disparados por CMS
export WEBHOOK_SECRET=...
uvicorn webhook_server:app --port 8080
```

Prueba el webhook en local:

```bash
curl -X POST http://localhost:8080/webhook/cdn-invalidate \
  -H "Content-Type: application/json" \
  -d '{"secret": "...", "type": "product_updated", "product_id": "123", "category_id": "456"}'
```
