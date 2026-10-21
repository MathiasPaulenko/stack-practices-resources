# Caching con Redis — Companion

Companion ejecutable de la [receta de caching con Redis](https://stackpractices.com/es/recipes/caching-redis/) en StackPractices. Los helpers de cache-aside y la protección contra stampede de la receta, organizados por stack:

| Archivo | Qué es |
|---------|--------|
| `python/cache_aside.py` | El decorador `cached()`, almacén de sesiones e invalidación manual. |
| `python/stampede.py` | Defensas contra stampede: lease lock + refresco temprano probabilístico. |
| `node/cache.js` | Helper `getCached()`, invalidación y rate limiter INCR/EXPIRE (ioredis). |
| `java/CacheClient.java` | Cliente Jedis con pool (`get`/`setex`). Las anotaciones `@Cacheable`/`@CacheEvict` de Spring aparecen en la receta — viven en la capa de servicio, no en un archivo aparte. |

## Requisitos

- Redis corriendo en local (`docker run -p 6379:6379 redis:7`)
- Python: `pip install redis`
- Node: `npm install ioredis`
- Java: `redis.clients:jedis` en el classpath

## Ejecutarlo

```bash
cd python && python cache_aside.py && python stampede.py
cd ../node && node cache.js
```

Receta original: https://stackpractices.com/es/recipes/caching-redis/
