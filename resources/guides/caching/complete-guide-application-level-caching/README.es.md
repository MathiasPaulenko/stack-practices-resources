# Caching a Nivel Aplicación — Companion

Ejemplos ejecutables de la [Guía Completa de Caching a Nivel Aplicación](https://stackpractices.com/es/guides/complete-guide-application-level-caching/).

## Archivos

- `lru_cache_decorator.py` — básicos de `functools.lru_cache`
- `lru_cache_ttl.py` — LRU con OrderedDict + TTL + RLock
- `lru_cache_node.js` — uso del paquete `lru-cache`
- `caffeine_cache.java` — builder de Caffeine con expiración + stats
- `redis_cache.py` — patrón `setex` + serialización JSON
- `memcached_cache.py` — cliente Memcached con valores serializados
- `two_tier_cache.py` — híbrida L1 memoria + L2 Redis
- `stampede_lock.py` — lock SET NX EX + double-check + reintento acotado
- `cache_sizing.py` — estimador de huella
- `threadsafe_cache.py` — dict protegido con RLock
- `concurrent_map.java` — ConcurrentHashMap + computeIfAbsent
- `node_cache.js` — caché Map simple (single-threaded)
- `cache_warming.py` — pre-poblado al arranque
- `resilient_cache.py` — fallback ante fallos de caché
- `monitored_cache.py` — contadores hit/miss + hit_rate

- `docker-compose.yaml` — Redis + Memcached locales (`docker compose up -d`)

## Uso

Requiere `redis`, `python-memcached`, `lru-cache` (npm), Caffeine (Java). Copia la implementación de tu nivel a tu app.

