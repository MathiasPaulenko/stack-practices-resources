# Nginx Reverse Proxy Cache — Companion

Runnable companion for the StackPractices recipe
[Cache HTTP Responses with Nginx Reverse Proxy](https://stackpractices.com/recipes/nginx-reverse-proxy-cache/).

## What's inside

| File | Purpose |
|---|---|
| `nginx.conf` | Complete caching reverse proxy: `proxy_cache_path` zone, TTL per status code, conditional bypass, cache lock, `use_stale`, background update, and a `/purge` endpoint |
| `docker-compose.yml` | Nginx + two `traefik/whoami` echo backends sharing a named volume for the cache zone |

## Quick start

```bash
docker compose up -d

curl -i http://localhost/api/hello                    # MISS — first request
curl -i http://localhost/api/hello                    # HIT  — served from cache
curl -i "http://localhost/api/hello?no_cache=1"       # BYPASS
curl -i -X POST http://localhost/api/hello            # BYPASS (non-GET)
curl -i -H "Authorization: Bearer x" http://localhost/api/hello  # BYPASS
```

Watch the `X-Cache-Status` header to see what Nginx did with each request.
To inspect the cache on disk, exec into the container:
`docker compose exec nginx ls /var/cache/nginx/api`.

## Notes

- The `/purge` endpoint needs the third-party `ngx_cache_purge` module or
  NGINX Plus. The stock `nginx:alpine` image does not include it — remove
  that location block if you use the stock image, and purge with
  `rm -rf` inside the cache volume instead.
- Both backends reply with their container name, so a `MISS` on the first
  request and an identical `HIT` on the second proves the body came from
  cache rather than a sticky upstream.

Source recipe: https://stackpractices.com/recipes/nginx-reverse-proxy-cache/
