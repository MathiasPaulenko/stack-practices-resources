# serverless-orchestration — Recursos complementarios

Código complementario para [Orquestación Serverless: Step Functions vs Temporal](https://stackpractices.com/es/recipes/serverless-orchestration/).

El mismo workflow de procesamiento de pedidos implementado en tres orquestadores: validar el pedido, comprobar inventario, cobrar el pago, fan-out a email y analytics, y programar el envío.

## Archivos

| Archivo | Lenguaje | Propósito |
|---------|----------|-----------|
| `order-workflow.json` | ASL (JSON) | Definición de la máquina de estados de AWS Step Functions |
| `order-workflow.ts` | TypeScript | Workflow de Temporal con actividades en paralelo |
| `order-orchestrator.py` | Python | Orquestador de Azure Durable Functions (modelo v2) |
| `order-saga.ts` | TypeScript | Saga de Temporal con transacciones de compensación |

## Requisitos

- **Step Functions**: cuenta de AWS y las funciones Lambda (`validateOrder`, `checkInventory`, `processPayment`, `sendEmail`, `updateAnalytics`, `scheduleShipment`, más `releaseInventory` y `notifyCustomer` para los caminos de fallo)
- **Temporal**: `@temporalio/workflow`, `@temporalio/activity` y un servidor de desarrollo (`temporal server start-dev`)
- **Durable Functions**: Python 3.9+, `azure-functions`, `azure-functions-durable` y Azure Functions Core Tools

## Inicio rápido

### Step Functions

```bash
# Validar la definición
aws stepfunctions create-state-machine \
  --name order-processing \
  --definition file://order-workflow.json \
  --role-arn arn:aws:iam::123456789:role/StepFunctionsRole

# Iniciar una ejecución
aws stepfunctions start-execution \
  --state-machine-arn arn:aws:states:us-east-1:123456789:stateMachine:order-processing \
  --input '{"id":"ord-1","items":[{"sku":"A","qty":1}],"total":49.99,"address":"..."}'
```

### Temporal

```bash
npm install @temporalio/workflow @temporalio/activity
temporal server start-dev   # servidor local de desarrollo
# Registra orderWorkflow en el task queue "orders" con un worker
# e inícialo con el cliente de Temporal o `temporal workflow start`.
```

### Durable Functions

```bash
pip install azure-functions azure-functions-durable
func start
curl http://localhost:7071/api/orchestrators/order_orchestrator
```

## Notas

- Reemplaza los ARNs de Lambda en `order-workflow.json` por los de tus funciones.
- `order-workflow.ts` y `order-saga.ts` esperan un módulo `activities.ts` que exporte las funciones de actividad — escribe el tuyo contra las firmas mostradas en cada archivo.
- Step Functions pasa payloads de hasta 256KB entre estados; para datos más grandes, guárdalos en S3 y pasa `{"bucket": ..., "key": ...}` por la máquina de estados.
