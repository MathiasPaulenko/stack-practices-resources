# Patrón de Enrutamiento de Gateway — Código Companion

Código companion del [Patrón de Enrutamiento de Gateway](https://stackpractices.com/es/patterns/gateway-routing-pattern/) en StackPractices.

Dos implementaciones de gateway funcionales que enrutan prefijos de ruta a servicios upstream:

- **`gateway.ts`** — Express + `http-proxy-middleware`. Añade middleware de ID de correlación, destinos proxy por ruta (configurables por variables de entorno), endpoint `/healthz` y manejador 502 para upstreams caídos.
- **`nginx.conf`** — El mismo enrutado en NGINX: bloques upstream, `proxy_set_header X-Request-ID` y endpoint de salud.
- **`docker-compose.yml`** — Demo ejecutable: gateway NGINX en `:8080` frente a tres upstreams `ealen/echo-server`.

## Inicio rápido

### NGINX + Docker (sin instalar código)

```bash
docker compose up
curl http://localhost:8080/users     # atendido por users-service
curl http://localhost:8080/orders    # atendido por orders-service
curl http://localhost:8080/inventory # atendido por inventory-service
curl http://localhost:8080/healthz   # salud del gateway
```

### Gateway Express

```bash
npm install
npm start
# Los upstreams por defecto son localhost:3001/3002/3003
# Sobrescríbelos con USERS_URL, ORDERS_URL, INVENTORY_URL
curl http://localhost:3000/users
```

## Notas

- El middleware de ID de correlación debe ejecutarse **antes** que las rutas proxy, o los upstreams nunca ven `X-Request-ID`.
- Los callbacks `router` pueden devolver un upstream distinto por solicitud — ese es el gancho para balanceo de carga y descubrimiento de servicios.
- Mantén el gateway sin estado: todas las decisiones de enrutado salen de la configuración y de la propia solicitud.
