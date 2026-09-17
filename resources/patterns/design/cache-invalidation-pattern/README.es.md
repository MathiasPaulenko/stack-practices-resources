# Patrón Cache Invalidation — Código complementario

Versiones ejecutables de las estrategias de invalidación del recurso
[Patrón Cache Invalidation](https://stackpractices.com/es/patterns/cache-invalidation-pattern/)
en StackPractices.

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `cache_invalidator.py` | Cuatro estrategias con Redis en Python: expiración TTL, invalidación explícita en escritura, pub/sub por eventos (`CacheInvalidator`) y claves versionadas |
| `cache-manager.ts` | `CacheManager` en TypeScript con invalidación por tags, versionada y write-through, más un `PubSubInvalidator` para despliegues multi-instancia |

## Requisitos

- Python: `pip install redis` (usa `fakeredis` para tests sin servidor)
- TypeScript: `redis` v4+ (`npm install redis`) y un servidor Redis
- `db` es un placeholder — conéctalo a tu propia capa de datos (ORM, helper de queries)

## Notas

- El cliente Python usa `decode_responses=True` para que `get()` devuelva `str`.
  Sin eso, las claves versionadas se rompen (`user:123:vb'1'`).
- `DEL` no expande comodines: `del("products:category:*")` solo borra una clave
  literal con ese nombre. Usa sets de tags o `scan_iter` para borrados agrupados.
