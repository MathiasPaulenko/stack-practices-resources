# Patrones de ThreadPoolExecutor — Codigo complementario

Patrones ejecutables para trabajo I/O en paralelo con `concurrent.futures`.

## Archivos

| Archivo | Que muestra |
|---|---|
| `thread_pool.py` | `collect_ordered` (map), `collect_as_completed` (submit + errores por future), `ThreadSafeResults` (colector compartido con lock), `session()` (requests.Session thread-local) y un smoke test en `__main__` — con sleep, sin red. |

## Inicio rapido

```bash
pip install -r requirements.txt
python thread_pool.py
# map: 8 results in 0.21s (~0.8s sequential)
# caught per-future: simulated API failure
```

## Fuente

- https://stackpractices.com/recipes/python-thread-pool-executor/
- https://stackpractices.com/es/recipes/python-thread-pool-executor/
