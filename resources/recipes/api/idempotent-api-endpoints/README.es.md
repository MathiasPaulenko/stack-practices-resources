# Endpoints de API Idempotentes — Recursos Companion

Código companion de la receta de StackPractices [Endpoints de API Idempotentes](https://stackpractices.com/es/recipes/idempotent-api-endpoints/).

## Contenidos

- `python_fastapi.py` — Implementación en Python FastAPI con store de idempotencia en memoria.
- `javascript_express.js` — Implementación en JavaScript Express con store basado en Map.
- `java_spring.java` — Implementación en Java Spring Boot con ConcurrentHashMap.
- `test_idempotency.py` — Tests de pytest cubriendo escenarios de duplicados, concurrencia y expiración de TTL.
- `requirements.txt` — Dependencias de Python.
- `meta.json` — Metadata del recurso.

## Ejecutar el ejemplo en Python

```bash
pip install -r requirements.txt
uvicorn python_fastapi:app --reload
```

## Ejecutar los tests

```bash
pip install -r requirements.txt
pytest test_idempotency.py -v
```

## Conceptos clave

- **Idempotency key**: UUID generado por el cliente y enviado en el header `Idempotency-Key`.
- **Estado processing**: previene que requests concurrentes con la misma clave ejecuten dos veces.
- **Limpieza TTL**: remueve entradas expiradas para evitar crecimiento sin límite del store.
- **Recuperación de errores**: remueve el marcador processing ante fallas para que el cliente pueda reintentar.
