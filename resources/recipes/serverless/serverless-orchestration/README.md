# serverless-orchestration — Companion Resources

Companion code for [Serverless Orchestration: Step Functions vs Temporal](https://stackpractices.com/recipes/serverless-orchestration/).

The same order-processing workflow implemented on three orchestrators: validate the order, check inventory, charge payment, fan out to email and analytics, then schedule shipment.

## Files

| File | Language | Purpose |
|------|----------|---------|
| `order-workflow.json` | ASL (JSON) | AWS Step Functions state machine definition |
| `order-workflow.ts` | TypeScript | Temporal workflow with parallel activities |
| `order-orchestrator.py` | Python | Azure Durable Functions orchestrator (v2 model) |
| `order-saga.ts` | TypeScript | Temporal saga with compensating transactions |

## Requirements

- **Step Functions**: AWS account, six Lambda functions (`validateOrder`, `checkInventory`, `processPayment`, `sendEmail`, `updateAnalytics`, `scheduleShipment`, plus `releaseInventory` and `notifyCustomer` for the failure paths)
- **Temporal**: `@temporalio/workflow`, `@temporalio/activity`, a Temporal dev server (`temporal server start-dev`)
- **Durable Functions**: Python 3.9+, `azure-functions`, `azure-functions-durable`, Azure Functions Core Tools

## Quick start

### Step Functions

```bash
# Validate the definition
aws stepfunctions create-state-machine \
  --name order-processing \
  --definition file://order-workflow.json \
  --role-arn arn:aws:iam::123456789:role/StepFunctionsRole

# Start an execution
aws stepfunctions start-execution \
  --state-machine-arn arn:aws:states:us-east-1:123456789:stateMachine:order-processing \
  --input '{"id":"ord-1","items":[{"sku":"A","qty":1}],"total":49.99,"address":"..."}'
```

### Temporal

```bash
npm install @temporalio/workflow @temporalio/activity
temporal server start-dev   # local dev server
# Register orderWorkflow on the "orders" task queue with a worker,
# then start it via the Temporal client or `temporal workflow start`.
```

### Durable Functions

```bash
pip install azure-functions azure-functions-durable
func start
curl http://localhost:7071/api/orchestrators/order_orchestrator
```

## Notes

- Replace the Lambda ARNs in `order-workflow.json` with your own function ARNs.
- `order-workflow.ts` and `order-saga.ts` expect an `activities.ts` module exporting the activity functions — write yours against the signatures shown in each file.
- Step Functions passes payloads up to 256KB between states; for larger data, store it in S3 and pass `{"bucket": ..., "key": ...}` through the state machine.
