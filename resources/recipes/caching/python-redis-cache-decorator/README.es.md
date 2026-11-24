# Cache de resultados de funciones con Redis y TTL en Python

Compañero ejecutable de la receta:
https://stackpractices.com/es/recipes/python-redis-cache-decorator/

## Contenido

- `cache_decorator.py` — decorador `@cached` (generacion determinista de claves desde la firma de la funcion, serializacion JSON, TTL configurable, `wrapper.cache_invalidate`), variante `async_cached` y helper `invalidate_tag`. El bloque `__main__` corre una prueba de humo de hit/miss/invalidacion contra un Redis local.

## Requisitos

- Python 3.10+
- Una instancia de Redis corriendo (`docker run -p 6379:6379 redis:7` es la opcion mas rapida)

## Instalacion y ejecucion

```bash
pip install -r requirements.txt
python cache_decorator.py
```

Salida esperada:

```text
{'id': '42', 'value': 'computed-42'}
{'id': '42', 'value': 'computed-42'}
{'id': '42', 'value': 'computed-42'}
OK: cache hit, miss, and invalidation all behave as expected
```

La segunda llamada sale de Redis (el contador se queda en 1); la llamada tras `cache_invalidate` recalcula.
