# AWS Step Functions Order Workflow

Runnable companion to the recipe
[Orchestrate Serverless Workflows with AWS Step Functions](https://stackpractices.com/recipes/serverless-step-functions-workflow/).

A complete order-processing state machine: validation, inventory check, a
choice branch on stock, payment with retry/catch, and shipping — deployed
with AWS SAM.

## Files

| File | Purpose |
|---|---|
| `order_workflow.asl.json` | Amazon States Language definition with `${...}` substitution placeholders |
| `template.yaml` | SAM template: state machine, 5 Lambda functions, least-privilege IAM role |
| `handlers.py` | Python task handlers (validate order, check inventory, process payment) |
| `start_execution.py` | `boto3` helper to start executions and poll their status |

## Deploy

```bash
sam build
sam deploy --guided
```

`DefinitionSubstitutions` in `template.yaml` fills the `${ValidateFunctionArn}`
style placeholders in the ASL file with real function ARNs at deploy time —
the same definition works across stages.

## Start an execution

```python
from start_execution import start_order_workflow
arn = start_order_workflow({"id": "ord-123", "items": [...], "customer": {...}})
```

Or from the console/CLI:

```bash
aws stepfunctions start-execution \
  --state-machine-arn <STATE_MACHINE_ARN> \
  --name order-demo-1 \
  --input '{"order":{"id":"ord-123"},"paymentMethod":{}}'
```

## Notes

- `handlers.py` references `check_stock` and `charge_payment` stubs — wire
  them to your inventory and payment providers before deploying.
- The template defaults to `STANDARD`; switch `Type:` to `EXPRESS` for
  high-throughput, sub-5-minute workflows.
