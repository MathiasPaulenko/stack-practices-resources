# Funciones Serverless Event-Driven — Companion

Companion ejecutable de la receta [Funciones Serverless Event-Driven](https://stackpractices.com/es/recipes/event-driven-functions/) en StackPractices.com.

## Archivos

| Archivo | Tipo | Contenido |
|---------|------|-----------|
| `handler.py` | Python | Lambda disparada por SQS con idempotencia (escritura condicional en DynamoDB) y respuesta de batch parcial con `batchItemFailures` |
| `template.yaml` | SAM | Infraestructura completa: regla de EventBridge en fan-out a dos Lambdas + SQS, DLQ con `redrivePolicy`, permisos de invocación, tabla de idempotencia |
| `publisher.mjs` | JavaScript (ESM) | Publicador `PutEvents` de EventBridge con `eventId` para deduplicación en el consumidor; ejecutable como script |

## Uso

```bash
sam deploy --guided            # despliega el stack
node publisher.mjs             # envía un evento OrderPlaced de prueba
sam logs -n PaymentFunction    # observa el consumidor
```

## Notas

- La regla de EventBridge hace match con `source: order-service` + `detail-type: OrderPlaced` — `DetailType` distingue mayúsculas.
- `batchItemFailures` es la diferencia entre reintentar un mensaje malo y reproducir todo el batch.
- `maxReceiveCount: 3` envía los poison messages a la DLQ tras tres recepciones fallidas.
