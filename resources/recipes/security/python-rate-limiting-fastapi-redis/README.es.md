# Rate limiting distribuido con FastAPI y Redis — Recursos Companion

Código companion para la [receta de Rate Limiting con FastAPI + Redis](https://stackpractices.com/es/recipes/python-rate-limiting-fastapi-redis/) en StackPractices.

## Contenidos

|Archivo|Descripción|
|---------|-------------|
|`sliding_window.py`|Rate limiter sliding window usando ZSET de Redis|
|`token_bucket.py`|Rate limiter token bucket usando script Lua de Redis|
|`fixed_window.py`|Rate limiter ventana fija usando INCR de Redis|
|`middleware.py`|Middleware de FastAPI + decorador por endpoint|
|`test_rate_limiting.py`|Tests unitarios para los tres limiters (usa fakeredis)|
|`README.md`|README en inglés|
|`README.es.md`|README en español|

## Cómo ejecutar los ejemplos

### Instalar dependencias

```bash
pip install fastapi redis uvicorn
pip install fakeredis pytest  # para tests
```

### Ejecutar la app FastAPI

```bash
uvicorn middleware:app --reload
```

### Ejecutar tests unitarios

```bash
pytest test_rate_limiting.py -v
```

## Algoritmos

|Algoritmo|Manejo de bursts|Precisión|Ops Redis|
|-----------|------------------|-----------|-----------|
|Sliding window|Sin bursts|Alta|ZSET pipeline|
|Token bucket|Bursts hasta capacity|Media|Script Lua|
|Fixed window|Bursts dobles en límite|Baja|INCR + EXPIRE|
