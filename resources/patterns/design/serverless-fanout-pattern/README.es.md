# Patrón Serverless Fanout

Código de acompañamiento del patrón de StackPractices:
<https://stackpractices.com/es/patterns/serverless-fanout-pattern/>

El patrón fanout difunde un solo evento a todos los consumidores suscritos a
través de un topic SNS. Cada consumidor tiene su propia cola SQS, así que un
consumidor lento o con fallos nunca bloquea a los demás — y el productor no
sabe quién está escuchando.

## Archivos

- `producer.py` — publica eventos `OrderPlaced` en el topic SNS con una clave
  de filtrado en `MessageAttributes`, para que los suscriptores filtren sin
  parsear el cuerpo.
- `consumer.py` — handler Lambda que procesa lotes SQS tratando el cuerpo del
  registro como JSON en crudo (entrega raw) y devuelve `batchItemFailures`
  para que solo se reintenten los registros fallidos.
- `template.yaml` — plantilla SAM con el topic SNS, dos colas SQS con DLQs y
  `maxReceiveCount: 3`, suscripciones con entrega raw (una con política de
  filtrado y otra sin) y las funciones consumidoras.

## Requisitos

- Python 3.11+ con `boto3`.
- Credenciales AWS con acceso a SNS/SQS/Lambda. Despliega con
  `sam deploy --guided` para crear el topic, las colas, las DLQs y las
  funciones.

## Uso

```python
from producer import publish_order_event

publish_order_event("order-123", "customer-42", 149.99)
# Cada cola suscrita recibe una copia; cada consumidor escala y falla de
# forma independiente. Los mensajes que fallan 3 veces van a la DLQ de esa cola.
```

## Notas

- La entrega es at-least-once: haz los consumidores idempotentes.
- Configura el `VisibilityTimeout` de la cola en al menos 6x el timeout del
  consumidor.
- Usa `RawMessageDelivery` para que los consumidores vean el JSON del evento
  y no el envelope de SNS — salvo que necesites los metadatos del envelope.
