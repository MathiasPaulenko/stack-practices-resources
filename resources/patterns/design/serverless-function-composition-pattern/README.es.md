# Patrón Serverless Function Composition

Código de acompañamiento del patrón de StackPractices:
<https://stackpractices.com/es/patterns/serverless-function-composition-pattern/>

La composición de funciones encadena funciones serverless en un workflow
coordinado. Un orquestador — AWS Step Functions aquí — es dueño de la
secuencia, los reintentos, el branching y el estado; cada Lambda es dueña
de un solo paso.

## Archivos

- `order_stack.py` — stack CDK (Python): cinco tasks `LambdaInvoke` unidas
  en una state machine con una rama `Choice`. El fallo de pago va a un paso
  de compensación (reembolso) y luego a `Fail`.
- `steps.py` — los cinco handlers Lambda (validar, pagar, reservar,
  notificar, reembolsar). Cada uno devuelve un dict que el orquestador pasa
  al siguiente estado.
- `state_machine.asl.json` — el mismo workflow como definición Amazon
  States Language, con un bloque `Retry` en la task de pago (solo
  excepciones de servicio, backoff exponencial).
- `start_execution.py` — lanza una ejecución con nombre único y consulta
  `describe_execution` para estado, output y error.

## Requisitos

- Python 3.11+ con `boto3`; `aws-cdk-lib` y `constructs` para el stack.
- Despliega con `cdk deploy` (o crea la state machine desde
  `state_machine.asl.json` apuntando `FunctionName` a tus funciones).

## Uso

```python
from start_execution import start_order_workflow, get_workflow_status

arn = start_order_workflow({
    "orderId": "order-123",
    "customerId": "customer-42",
    "items": [{"productId": "A1", "quantity": 2, "price": 74.99}],
    "total": 149.98,
})
print(get_workflow_status(arn))
```

## Notas

- Mantén cada paso idempotente: el orquestador puede reintentar una task.
- Step Functions limita el input/output de estado a 256KB — pasa
  referencias (S3 keys, IDs), no payloads completos.
- No pongas `retry_on_failure` en el construct `StateMachine` — no es una
  prop válida. Los reintentos van en las tasks o en `Retry`/`Catch` de ASL.
