# Nginx Reverse Proxy y API Gateway — Companion

Entorno ejecutable para la receta
[Configura Nginx como Reverse Proxy y API Gateway](https://stackpractices.com/es/recipes/nginx-reverse-proxy/)
([English version](https://stackpractices.com/recipes/nginx-reverse-proxy/)).

## Qué incluye

- `nginx.conf` — config de gateway en un solo archivo: zona de rate limiting,
  pool upstream con servidor de backup, routing por path, headers reenviados,
  endpoint `/health` servido por el propio Nginx y failover con
  `proxy_next_upstream`.
- `docker-compose.yml` — Nginx más tres backends `traefik/whoami`, para ver el
  balanceo de carga y el failover funcionando de verdad.

## Pruébalo

```bash
docker compose up -d

# Endpoint de salud del propio Nginx
curl http://localhost:8080/health

# Routing por path -> siempre cae en backend1
curl http://localhost:8080/api/users/

# Balanceo de carga -> whoami responde con un hostname distinto cada vez
curl http://localhost:8080/api/

# Rate limiting (10 r/s, burst 20) -> mira cómo aparecen los 429
for i in $(seq 40); do curl -o /dev/null -s -w "%{http_code}\n" http://localhost:8080/api/; done
```

## Valida antes de recargar

```bash
docker compose exec nginx nginx -t
docker compose exec nginx nginx -s reload
```

## Limpieza

```bash
docker compose down
```
