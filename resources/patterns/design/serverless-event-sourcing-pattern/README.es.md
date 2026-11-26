# Patrón Serverless Event Sourcing

Código acompañante del patrón de StackPractices:
<https://stackpractices.com/es/patterns/serverless-event-sourcing-pattern/>

Event sourcing almacena el estado de la aplicación como un log append-only
de eventos inmutables. En AWS, DynamoDB actúa de event store, DynamoDB
Streams dispara la Lambda de proyección y EventBridge reparte los eventos a
los consumidores downstream.

## Archivos

- `event_store.py` — `EventStore` en Python sobre DynamoDB: append con
  concurrencia optimista (escritura condicional sobre `aggregateId` +
  `version`), consultas ordenadas y replay para reconstruir el estado.
- `projection_handler.py` — Lambda disparada por el stream de la tabla que
  proyecta el estado a `order_projection`, con upserts idempotentes por
  versión entrante.
- `event-store.ts` — variante TypeScript que además publica cada evento a
  EventBridge para los consumidores downstream.
- `template.yaml` — plantilla SAM con la tabla `event_store` (streams +
  PITR), el read model `order_projection` y la función de proyección
  conectada al stream.

## Requisitos

- Python 3.11+ con `boto3`, o Node.js 18+ con `@aws-sdk/client-dynamodb`,
  `@aws-sdk/client-eventbridge` y `@aws-sdk/util-dynamodb`.
- Credenciales AWS con acceso a DynamoDB. Despliega `template.yaml` con
  `sam deploy --guided` para crear las tablas y la función de proyección.

## Uso

```python
from event_store import create_order, confirm_order, get_order_state

create_order("order-1", "customer-42", [{"sku": "A1", "qty": 2}])
confirm_order("order-1")
print(get_order_state("order-1"))
# {'customerId': 'customer-42', 'items': [...], 'status': 'CONFIRMED', 'version': 2}
```

La función de proyección corre sola con cada INSERT del stream — no hace
falta dispararla manualmente una vez desplegada.
