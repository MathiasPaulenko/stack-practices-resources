# Gateway Routing Pattern — Companion Code

Companion code for [Gateway Routing Pattern](https://stackpractices.com/patterns/gateway-routing-pattern/) on StackPractices.

Two working gateway implementations that route path prefixes to upstream services:

- **`gateway.ts`** — Express + `http-proxy-middleware`. Adds a correlation ID middleware, per-route proxy targets (configurable via env vars), a `/healthz` endpoint, and a 502 handler for dead upstreams.
- **`nginx.conf`** — The same routing in NGINX: upstream blocks, `proxy_set_header X-Request-ID`, and a health endpoint.
- **`docker-compose.yml`** — Runnable demo: NGINX gateway on `:8080` in front of three `ealen/echo-server` upstreams.

## Quick start

### NGINX + Docker (no code to install)

```bash
docker compose up
curl http://localhost:8080/users     # handled by users-service
curl http://localhost:8080/orders    # handled by orders-service
curl http://localhost:8080/inventory # handled by inventory-service
curl http://localhost:8080/healthz   # gateway health
```

### Express gateway

```bash
npm install
npm start
# Upstreams default to localhost:3001/3002/3003
# Override with USERS_URL, ORDERS_URL, INVENTORY_URL
curl http://localhost:3000/users
```

## Notes

- The correlation ID middleware must run **before** the proxy routes, or upstreams never see `X-Request-ID`.
- `router` callbacks can return a different upstream per request — that's the hook for load balancing and service discovery.
- Keep the gateway stateless: all routing decisions come from config and the request itself.
