# Patrón Correlation ID — Archivos complementarios

Artefactos ejecutables del [patrón Correlation ID](https://stackpractices.com/es/patterns/correlation-id-pattern/) en StackPractices.

## Archivos

| Archivo | Qué muestra |
|---------|-------------|
| `correlation_middleware.py` | Middleware FastAPI: generar-o-reutilizar en el borde, almacenamiento con `contextvars`, filtro de logging JSON estructurado |
| `correlation-middleware.mjs` | Middleware Node/Express con `AsyncLocalStorage` — el ID sobrevive a los `await` sin pasar `req` a los helpers |
| `rabbitmq_correlation.py` | Publisher + consumer RabbitMQ: ID en headers del mensaje Y en metadata del body, extracción con fallback |
| `CorrelationIdFilter.java` | `OncePerRequestFilter` de Spring Boot + MDC + interceptor de `RestTemplate` para propagar a llamadas descendentes |

## Inicio rápido

```bash
# FastAPI
pip install fastapi uvicorn
uvicorn correlation_middleware:app --reload
curl -i http://localhost:8000/orders -H "X-Correlation-ID: demo-123"

# Node (el servidor demo no necesita dependencias)
node correlation-middleware.mjs
curl -i http://localhost:3000/orders -H "x-correlation-id: demo-123"

# RabbitMQ (necesita un broker local)
pip install pika
python rabbitmq_correlation.py
```

Los servicios demo devuelven el correlation ID en los headers de respuesta y lo imprimen en cada línea de log —envía tu propio `X-Correlation-ID` y mira cómo sobrevive, u omítelo y verás cómo se genera un UUID.

- Doc: https://stackpractices.com/es/patterns/correlation-id-pattern/
- Doc (EN): https://stackpractices.com/patterns/correlation-id-pattern/
