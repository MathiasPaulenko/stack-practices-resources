# Cachear Respuestas HTTP con httpx y CacheControl — Archivos complementarios

Ejemplos ejecutables de la receta
[Cachear Respuestas HTTP con httpx y CacheControl en Python](https://stackpractices.com/es/recipes/python-httpx-cache-responses/).

## Archivos

- `client.py` — factories de cliente con backend de archivos y Redis, más el wrapper `CachedHttpClient` con force-refresh y límite de TTL. Incluye una demo en `__main__` contra `httpbin.org/cache/60`.
- `requirements.txt` — `httpx`, `cachecontrol[filecache]`, `redis`.

## Uso

```bash
pip install -r requirements.txt
python client.py
```

La demo llama a `https://httpbin.org/cache/60`, un endpoint que responde con `Cache-Control: max-age=60`. La primera petición descarga de la red; la segunda imprime `from_cache=True`.
