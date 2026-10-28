# Patrón Cache Stampede Prevention — Simulaciones ejecutables

Companion del patrón de StackPractices [Patrón Cache Stampede Prevention](https://stackpractices.com/es/patterns/cache-stampede-prevention-pattern/).

Un simulador de stampede en dos lenguajes: 20 llamadores concurrentes golpean una key caliente expirada contra un store en memoria que reproduce la semántica de Redis (`GET`, `SETEX`, `SET NX EX`, liberación check-and-delete). Solo stdlib — no necesitas servidor Redis ni dependencias.

## Archivos

| Archivo | Stack | Ejecutar |
| --- | --- | --- |
| `src/stampede_demo.py` | Python 3.10+ (solo stdlib) | `python src/stampede_demo.py` |
| `src/stampede-demo.ts` | Node 20+ / tsx | `npx tsx src/stampede-demo.ts` |

Cada ejecución compara una lectura cache-aside ingenua (~20 queries a la base de datos) con las estrategias protegidas — single-flight en memoria, lock distribuido y stale-while-revalidate — imprimiendo el número de queries por estrategia. Resultado esperado: las estrategias protegidas colapsan la ráfaga a ~1 query.

Las clases `MiniRedis`/`FakeDB` son deliberadamente en memoria para que la demo corra en cualquier lado; el código de coordinación (locks, eventos, double-check, ventana stale) refleja las implementaciones de producción del artículo.
