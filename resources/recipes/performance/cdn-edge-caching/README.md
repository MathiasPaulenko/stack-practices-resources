# CDN Edge Caching — Companion Code

Multi-provider edge caching configuration for Cloudflare, AWS CloudFront,
and Fastly. Source: <https://stackpractices.com/recipes/cdn-edge-caching/>

## Files

| File | Provider | What it does |
| --- | --- | --- |
| `cloudfront.tf` | AWS CloudFront | Distribution + cache policy with an empty `parameters_in_cache_key` — headers, cookies, and query strings excluded so hit ratio stays high |
| `cloudflare-cache-rules.sh` | Cloudflare | Creates a zone ruleset (`http_request_cache_settings` phase) that pins a 30-day edge TTL for static assets |
| `fastly.vcl` | Fastly | `vcl_recv`/`vcl_fetch` marking static extensions immutable + `Surrogate-Key: static` for scoped purges |
| `purge.sh` | All three | Purge by path (CloudFront), URL (Cloudflare), or surrogate key (Fastly) |

## Usage

```bash
# CloudFront
terraform plan && terraform apply
aws cloudfront create-invalidation --distribution-id E1EXAMPLE --paths "/assets/*"

# Cloudflare
export ZONE_ID=... API_TOKEN=...
./cloudflare-cache-rules.sh

# Fastly
# upload fastly.vcl to your service version, then:
./purge.sh fastly static
```

## Notes

- Page Rules are deprecated; the Cloudflare script uses the Ruleset Engine.
- Cloudflare tag purging requires an Enterprise plan; the script purges by URL.
- `stale-while-revalidate` / `stale-if-error` belong on the origin's
  `Cache-Control` header, not in the CDN config.
