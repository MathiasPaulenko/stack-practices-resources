# Prevención de Race Conditions — Companion

Versiones ejecutables de los seis patrones de la
[recipe de prevención de race conditions](https://stackpractices.com/es/recipes/race-condition-prevention/).
Cada archivo corresponde a una solución numerada de la recipe.

## Archivos

| Archivo | Patrón | Qué previene |
|---------|--------|--------------|
| `search_service.ts` | AbortController | Una respuesta obsoleta pisando los resultados de una query más nueva |
| `atomic_counter.ts` | Cola de promises serializada | Incrementos perdidos a través de un `await` |
| `use_latest_query.ts` | Request IDs (solo-última) | Renderizar el perdedor de una carrera desordenada |
| `mutex.ts` | Mutex FIFO | Intercalación de check-and-act sobre estado compartido |
| `cas_store.ts` | Compare-and-swap | Escrituras a ciegas; reintenta solo si el valor cambió |
| `asyncio_transfer.py` | `asyncio.Lock` | La misma race check-and-act en servicios Python |

## Ejecución

```bash
python asyncio_transfer.py          # A: 600, B: 900 — cada transferencia serializada
npx tsx mutex.ts                    # los .ts corren con tsx/ts-node
```

## Notas

- `asyncio_transfer.py` solo necesita Python 3.8+, sin dependencias.
- Los `.ts` son snippets autocontenidos: `use_latest_query.ts` espera React
  (hook con `useCallback`/`useRef`); el resto no usa framework.
- Single-threaded no significa libre de races: cada `await` es un punto de
  cesión donde otra tarea puede colarse entre tu comprobación y tu escritura.
