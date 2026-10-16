# Trazado distribuido: OpenTelemetry, Jaeger y Zipkin

Código complementario de la guía [Trazado distribuido: OpenTelemetry, Jaeger y Zipkin](https://stackpractices.com/es/guides/complete-guide-distributed-tracing/).

## Contenido

| Archivo | Qué muestra |
|---------|-------------|
| `instrumentation.py` | TracerProvider + BatchSpanProcessor + exportador OTLP, auto-instrumentación para Flask/requests/SQLAlchemy/Redis |
| `order_service.py` | Spans manuales con anidación padre-hijo y registro de errores |
| `tracing.ts` | NodeSDK de Node.js, auto-instrumentaciones, patrón de span manual con `context.with` |
| `kafka_propagation.py` | Propagación del contexto de traza por los headers de mensajes de Kafka (inject/extract) |
| `span_links.py` | Span links para consumidores por lotes — asocia trazas sin anidar |
| `otel-collector-config.yaml` | Collector de producción: memory_limiter, filtro de health checks, atributos de recurso, lotes |
| `docker-compose.yml` | Laboratorio con Jaeger all-in-one + Zipkin + OTel Collector |

## Inicio rápido

```bash
# Levanta Jaeger, Zipkin y el collector
docker compose up -d

# Envía algunos spans (cualquier app OTLP apuntando a localhost:14317)
# y abre http://localhost:16686 para buscar tu servicio
```

## Notas

- Los ejemplos de Python necesitan `opentelemetry-sdk`, `opentelemetry-exporter-otlp`, los paquetes `opentelemetry-instrumentation-*` de tu framework, y `kafka-python` para el productor/consumidor.
- `tracing.ts` necesita `@opentelemetry/sdk-node`, `@opentelemetry/exporter-trace-otlp-grpc` y los paquetes `instrumentation-*` de sus imports.
- La vía del agente Java (`-javaagent:opentelemetry-javaagent.jar`) se cubre en la guía en lugar de un archivo suelto — es configuración, no código.
