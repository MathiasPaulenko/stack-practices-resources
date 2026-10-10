# Peticiones HTTP concurrentes con asyncio.gather y aiohttp

Recurso complementario de [Peticiones HTTP concurrentes con asyncio.gather y aiohttp](https://stackpractices.com/es/recipes/python-async-gather-concurrent-requests/).

## Archivos

- `fetch_all.py` — obtiene varios endpoints en paralelo con un semáforo, timeouts por petición y captura de errores con `return_exceptions`.
- `requirements.txt` — la única dependencia es `aiohttp`.

## Uso

```bash
pip install -r requirements.txt
python fetch_all.py
```

Salida esperada: las cinco peticiones terminan aproximadamente en el tiempo de la más lenta (~2s) en lugar de los ~5s que tardaría un bucle secuencial.

## Qué demuestra

- `asyncio.gather` con `return_exceptions=True` para que un fallo no cancele al resto.
- `asyncio.Semaphore` para acotar las peticiones en vuelo.
- `aiohttp.ClientTimeout` con plazos totales y de conexión.
- Una `ClientSession` compartida para reutilizar las conexiones TCP.
