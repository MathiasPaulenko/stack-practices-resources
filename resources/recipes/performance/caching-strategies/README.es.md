# Estrategias de Caché — Código complementario

Ejemplos ejecutables de la receta [Estrategias de Caché: Navegador, CDN, Redis y Base de Datos](https://stackpractices.com/es/recipes/caching-strategies/).

## Archivos

| Archivo | Capa | Qué muestra |
|---------|------|-------------|
| `cache-aside.js` | Aplicación | Cache-aside con Redis en Node.js (caché → DB → poblar) |
| `stampede-lock.js` | Aplicación | Protección anti-stampede con `SET NX EX`; solo una petición reconstruye |
| `swr.js` | Aplicación | Stale-while-revalidate sobre Redis con flag de obsoleto |
| `multi-level-cache.py` | Aplicación | L1 en proceso + L2 Redis + L3 base de datos |
| `event-invalidation.py` | Aplicación | Invalidación por Pub/Sub al escribir, sin compromiso de TTL |
| `cache-warming.py` | Aplicación | Pre-poblado asíncrono de claves calientes post-despliegue |
| `nginx-cache.conf` | Proxy | `proxy_cache` + `proxy_cache_use_stale` + cabeceras de assets |
| `sw.js` | Navegador | Service Worker con estrategia cache-first y limpieza de versiones |
| `materialized-view.sql` | Base de datos | Ajuste del buffer pool, vista materializada y chequeo de hit ratio |

## Requisitos

- Node.js 18+ con `redis` (`npm install redis`)
- Python 3.9+ con `redis` (`pip install redis`)
- Redis en `localhost:6379` (ej. `docker run -p 6379:6379 redis:7`)
- Nginx 1.18+ para `nginx-cache.conf`
- PostgreSQL 12+ para `materialized-view.sql`

## Inicio rápido

```bash
npm install redis
node cache-aside.js      # MISS y luego HIT
node stampede-lock.js   # 5 peticiones concurrentes, una sola reconstrucción
```

```bash
pip install redis
python multi-level-cache.py
python event-invalidation.py
python cache-warming.py
```
