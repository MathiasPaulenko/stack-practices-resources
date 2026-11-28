# Patrón Thread Pool — Companion

Ejemplos ejecutables en Python del artículo del patrón Thread Pool: pool fijo con `submit`/`as_completed`, `executor.map`, manejo de errores por future y la fórmula de dimensionado de Goetz. Todas las tareas son I/O simulada (con sleep) — nada toca la red.

## Archivos

- `thread_pool_examples.py` — los ejemplos del artículo, ejecutables de forma autónoma.
- `test_thread_pool.py` — tests pytest de los ejemplos.
- `requirements.txt` — dependencia de test.

## Ejecutar

```bash
pip install -r requirements.txt
python thread_pool_examples.py   # imprime resultados por tarea
pytest test_thread_pool.py       # 3 tests
```

Artículo fuente: https://stackpractices.com/es/patterns/thread-pool-pattern/
