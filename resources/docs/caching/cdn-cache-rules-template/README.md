# CDN Cache Rules Template

Companion code for [CDN Cache Rules Template](https://stackpractices.com/docs/cdn-cache-rules-template/).

## Contents

| File | What it is |
|------|------------|
| `cloudflare-purge.py` | Purge helpers: by URL, by cache tag, and full post-deploy purge (`purge_after_deploy`) |
| `cdn-health-check.py` | Hit ratio + bandwidth report with a <90% alert, via Cloudflare analytics |
| `nginx-cache-headers.conf` | Origin `Cache-Control` headers per content type (HTML, versioned assets, API, sitemaps) |

## How to use

- Python files need `pip install requests`; set `CLOUDFLARE_ZONE_ID` and `CLOUDFLARE_API_TOKEN`.
- Copy the nginx blocks into your origin server config.
