# Caché con Nginx Reverse Proxy — Companion

Ejemplo ejecutable del recurso de StackPractices
[Cachear Respuestas HTTP con Nginx Reverse Proxy](https://stackpractices.com/es/recipes/nginx-reverse-proxy-cache/).

## Qué incluye

| Archivo | Propósito |
|---|---|
| `nginx.conf` | Reverse proxy con caché completo: zona `proxy_cache_path`, TTL por código de estado, bypass condicional, cache lock, `use_stale`, background update y endpoint `/purge` |
| `docker-compose.yml` | Nginx + dos backends echo `traefik/whoami` con un volumen compartido para la zona de caché |

## Inicio rápido

```bash
docker compose up -d

curl -i http://localhost/api/hello                    # MISS — primera petición
curl -i http://localhost/api/hello                    # HIT  — servida desde caché
curl -i "http://localhost/api/hello?no_cache=1"       # BYPASS
curl -i -X POST http://localhost/api/hello            # BYPASS (no es GET)
curl -i -H "Authorization: Bearer x" http://localhost/api/hello  # BYPASS
```

Mira el header `X-Cache-Status` para ver qué hizo Nginx con cada petición.
Para inspeccionar el caché en disco, entra al contenedor:
`docker compose exec nginx ls /var/cache/nginx/api`.

## Notas

- El endpoint `/purge` necesita el módulo de terceros `ngx_cache_purge` o
  NGINX Plus. La imagen estándar `nginx:alpine` no lo incluye — elimina ese
  location si usas la imagen oficial y purga con `rm -rf` dentro del
  volumen de caché.
- Los dos backends responden con su nombre de contenedor, así que un `MISS`
  en la primera petición y un `HIT` idéntico en la segunda demuestran que
  el cuerpo vino del caché y no de un upstream fijo.

Recurso original: https://stackpractices.com/es/recipes/nginx-reverse-proxy-cache/
