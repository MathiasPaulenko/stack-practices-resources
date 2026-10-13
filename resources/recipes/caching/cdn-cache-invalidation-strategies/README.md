# CDN Cache Invalidation Strategies — Companion Files

Runnable companion code for the StackPractices recipe
[CDN Cache Invalidation Strategies and Patterns](https://stackpractices.com/recipes/cdn-cache-invalidation-strategies/).

## Files

- `cdn_invalidate.py` — purge helpers for Cloudflare (URLs, cache tags, purge everything), Fastly (URLs, surrogate keys, soft purge) and AWS CloudFront (path invalidations), plus a deploy hook driven by `CDN_PROVIDER`.
- `webhook_server.py` — FastAPI endpoint that receives CMS events (`product_updated`, `full_deploy`) and calls the right purge. Requires `WEBHOOK_SECRET` plus the provider credentials.

## Usage

```bash
pip install httpx boto3 fastapi uvicorn

# Purge everything on deploy
export CDN_PROVIDER=cloudflare
export CLOUDFLARE_ZONE_ID=... CLOUDFLARE_API_TOKEN=...
python cdn_invalidate.py

# Or run the webhook for CMS-triggered purges
export WEBHOOK_SECRET=...
uvicorn webhook_server:app --port 8080
```

Test the webhook locally:

```bash
curl -X POST http://localhost:8080/webhook/cdn-invalidate \
  -H "Content-Type: application/json" \
  -d '{"secret": "...", "type": "product_updated", "product_id": "123", "category_id": "456"}'
```
