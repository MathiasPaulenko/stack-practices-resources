# Complete Guide to CDN Caching Strategy — Companion Code

Runnable building blocks for the guide
[Complete Guide to CDN Caching Strategy](https://stackpractices.com/guides/complete-guide-cdn-caching-strategy/)
on StackPractices.

## Files

| File | What it implements |
| --- | --- |
| `nginx-cache-headers.conf` | Header matrix per content type |
| `worker-cache-key-normalizer.js` | Cloudflare Worker: strip tracking params |
| `surrogate_key_purge.py` | Fastly surrogate-key + Cloudflare URL purge |
| `event_purge.py` | Purge after write (event-driven invalidation) |
| `hit_ratio.py` | Hit-ratio calculator + per-type targets |
| `cdn_failover.sh` | Route53 DNS failover health check |
| `test_hit_ratio.py` | pytest smoke tests |

## Setup

```bash
pip install -r requirements.txt
pytest test_hit_ratio.py -v
```

API keys come from env vars (`FASTLY_API_KEY`, `CF_API_TOKEN`); `db_products`
is your app data layer.
