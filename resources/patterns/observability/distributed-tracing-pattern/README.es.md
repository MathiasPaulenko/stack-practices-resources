# Patrón de Trazado Distribuido — Archivos complementarios

Ejemplos ejecutables del [patrón de trazado distribuido](https://stackpractices.com/es/patterns/distributed-tracing-pattern/) de StackPractices.

## Archivos

| Archivo | Qué muestra |
|---------|-------------|
| `otel_setup.py` | Tracer provider compartido: identidad del recurso, exportación OTLP, muestreo `ParentBased` + `TraceIdRatioBased` |
| `fastapi_traced_app.py` | Servicio FastAPI con las dos mitades — el middleware extrae `traceparent` entrante, el handler lo inyecta saliente |
| `rabbitmq_propagation.py` | Productor/consumidor RabbitMQ: contexto en las cabeceras del mensaje, extraído al consumir para unir los spans |
| `otel-collector-config.yaml` | Pipeline del collector: entrada OTLP, salida `otlp/jaeger` + Zipkin + Tempo, políticas de muestreo de cola |

## Inicio rápido

```bash
pip install -r requirements.txt

# Terminal 1 — un backend de trazas (Jaeger all-in-one acepta OTLP en 4317)
docker run -p 16686:16686 -p 4317:4317 -p 4318:4318 jaegertracing/all-in-one:latest

# Terminal 2 — servicio FastAPI (extract + inject)
uvicorn fastapi_traced_app:app --port 8000
curl -X POST "http://localhost:8000/orders?order_id=ord_42" \
  -H 'traceparent: 00-0af7651916cd43dd8448eb211c80319c-b7ad6b7169203331-01'

# Demo de RabbitMQ (necesita un broker en 5672)
docker run -d -p 5672:5672 rabbitmq:3
python rabbitmq_propagation.py
```

Abre `http://localhost:16686` y busca los servicios `order-service` / `orders-worker` — el span del consumidor aparece como hijo del span de publicación dentro de la misma traza.

- Doc: https://stackpractices.com/patterns/distributed-tracing-pattern/
- Doc (ES): https://stackpractices.com/es/patterns/distributed-tracing-pattern/
