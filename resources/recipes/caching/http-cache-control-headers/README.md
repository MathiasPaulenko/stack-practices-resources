# HTTP Cache-Control Headers — Companion Files

Working configs for the main patterns in the recipe: long-lived `immutable` caching for hashed static assets, short `max-age` with `stale-while-revalidate` for public API responses, conditional requests with `ETag` and `Last-Modified`, and `no-store`/`private` for sensitive data.

Source article: [HTTP Cache-Control Headers for APIs and Static Assets](https://stackpractices.com/recipes/http-cache-control-headers/)

## Files

| File | Role |
|------|------|
| `nginx.conf` | Server block with per-location `Cache-Control`: `immutable` assets, `no-cache` HTML, `stale-while-revalidate` API, `private`/`no-store` auth routes. |
| `express-cache-headers.js` | Express app implementing every variant: static `maxAge`, ETag conditional responses, `Last-Modified` date comparison, split `s-maxage`, `Vary`. |
| `fastapi-cache-headers.py` | FastAPI app with a middleware that sets `Cache-Control` on `/static/` (because `StaticFiles` doesn't accept `max_age`) plus an ETag example. |

## Usage

```bash
# Express (Node 18+)
npm install express
node express-cache-headers.js
curl -I http://localhost:3000/api/products            # see Cache-Control + ETag
curl -I -H 'If-None-Match: "<etag>"' http://localhost:3000/api/products  # 304

# FastAPI
pip install fastapi uvicorn
uvicorn fastapi-cache-headers:app
curl -I http://localhost:8000/api/products

# nginx — drop the server block into your config and reload
nginx -t && nginx -s reload
curl -I http://localhost/api/products
```

Verify headers with `curl -I` or the Network tab in DevTools: look for `Cache-Control`, `ETag`, `Last-Modified`, `Age`, and `X-Cache`.
