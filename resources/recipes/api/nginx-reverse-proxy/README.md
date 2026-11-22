# Nginx Reverse Proxy & API Gateway — Companion

Runnable playground for the recipe
[Configure Nginx as a Reverse Proxy and API Gateway](https://stackpractices.com/recipes/nginx-reverse-proxy/)
([versión en español](https://stackpractices.com/es/recipes/nginx-reverse-proxy/)).

## What's inside

- `nginx.conf` — a single-file gateway config: rate limiting zone, upstream pool
  with a backup server, path-based routing, forwarded headers, a `/health`
  endpoint served by Nginx itself, and `proxy_next_upstream` failover.
- `docker-compose.yml` — Nginx plus three `traefik/whoami` echo backends, so you
  can watch load balancing and failover actually happen.

## Try it

```bash
docker compose up -d

# Nginx's own health endpoint
curl http://localhost:8080/health

# Path routing -> always lands on backend1
curl http://localhost:8080/api/users/

# Load balancing -> whoami answers with a different hostname each time
curl http://localhost:8080/api/

# Rate limiting (10 r/s, burst 20) -> watch the 429s kick in
for i in $(seq 40); do curl -o /dev/null -s -w "%{http_code}\n" http://localhost:8080/api/; done
```

## Validate before reloading

```bash
docker compose exec nginx nginx -t
docker compose exec nginx nginx -s reload
```

## Tear down

```bash
docker compose down
```
