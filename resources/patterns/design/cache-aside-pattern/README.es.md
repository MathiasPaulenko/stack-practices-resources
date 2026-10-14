# Patrón Cache-Aside — Código complementario

Versiones ejecutables de las implementaciones cache-aside del recurso
[Patrón Cache-Aside](https://stackpractices.com/es/patterns/cache-aside-pattern/)
en StackPractices.

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `cache_aside.py` | `CacheAside` en Python sobre Redis: TTL en cada clave, invalidación en escritura y un lock de llenado `SET NX PX` para que un stampede de caché frío produzca una sola consulta en vez de N |
| `cache-aside.ts` | `CacheAside` en TypeScript para redis v4: deduplicación de promesas (single-flight) en misses concurrentes, TTL con `setEx`, invalidación en escritura |

## Requisitos

- Python: `pip install redis` (`pip install fakeredis` para correr la demo sin servidor)
- TypeScript: `redis` v4+ (`npm install redis`) y un servidor Redis
- `db` es un placeholder — conéctalo a tu propia capa de datos (psycopg, pg, Prisma)

## Notas

- La invalidación elimina la clave en vez de actualizarla: la próxima
  lectura se autocorrige y solo hay un camino de escritura que mantener.
- El TTL es la red de seguridad para eventos de invalidación perdidos —
  no sustituye a eliminar la clave en las escrituras.
- Ambas implementaciones protegen el camino del miss: la de Python usa un
  lock de corta duración y la de TypeScript reutiliza la promesa en curso.
