# Patrón de Throttling Serverless

Companion ejecutable del patrón
[Patrón de Throttling Serverless](https://stackpractices.com/es/patterns/serverless-throttling-pattern/).

Tres formas complementarias de proteger servicios de destino frente a picos
de tráfico de Lambda: un consumidor SQS con tope de concurrencia, un token
bucket en DynamoDB y el stack CDK que conecta cola + consumidor + DLQ.

## Archivos

| Archivo | Propósito |
|---|---|
| `sqs_consumer.py` | Consumidor Lambda con reporte de fallos parciales del lote (`batchItemFailures`) y sondeo de capacidad de destino |
| `token_bucket.ts` | Token bucket sobre DynamoDB que aplica una tasa de peticiones precisa por clave |
| `throttled_consumer_stack.py` | Stack CDK (Python): cola con long polling + DLQ, consumidor topado a 10 ejecuciones concurrentes |

## Notas

- `sqs_consumer.py` referencia un stub `api_client` — conéctalo a tu cliente
  real (`requests`, `httpx`) antes de desplegar.
- La concurrencia reservada se dimensiona desde el límite del destino, no
  del tráfico: tamaño del pool menos margen para otros llamantes.
- El token bucket falla cerrado ante errores de DynamoDB por defecto.
  Envuelve `allowRequest` y falla abierto para endpoints no críticos.
