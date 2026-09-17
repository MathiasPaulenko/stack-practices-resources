# Patrón Write-Behind Cache — Código complementario

Versiones ejecutables de las implementaciones write-behind del recurso
[Patrón Write-Behind Cache](https://stackpractices.com/es/patterns/write-behind-cache-pattern/)
en StackPractices.

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `write_behind_cache.py` | `WriteBehindCache` en Python con dirty set durable en Redis, toma atómica del volcado vía `RENAME`, ejemplo de upsert en lote y demo con fakeredis |
| `write-behind-cache.ts` | `WriteBehindCache` en TypeScript con el mismo dirty set en Redis, escrituras pipelineadas con `multi()` y un escritor por lotes Postgres `ON CONFLICT` |

## Requisitos

- Python: `pip install redis` (`pip install fakeredis` para la demo sin servidor)
- TypeScript: `redis` v4+ (`npm install redis`) y un servidor Redis
- `db` es un placeholder — conéctalo a tu propia capa de datos (psycopg, pg, Prisma)

## Notas

- El dirty set se guarda en Redis (`writebehind:dirty`), no en la memoria
  del proceso, así que un crash de la aplicación no pierde la cola de
  volcado. El propio Redis aún necesita persistencia (AOF `everysec` o
  RDB+AOF) para acotar la ventana de pérdida si cae el servidor.
- `RENAME dirty → flushing` toma atómicamente el conjunto pendiente, de modo
  que las escrituras que llegan durante un volcado se recogen en el
  siguiente ciclo.
- Mantén los TTL muy por encima del peor lag de volcado — una clave que
  expira o se evicte estando pendiente es una escritura perdida en silencio.
