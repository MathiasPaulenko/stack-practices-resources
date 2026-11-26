# Serverless Function Composition Pattern

Companion code for the StackPractices pattern:
<https://stackpractices.com/patterns/serverless-function-composition-pattern/>

Function composition chains serverless functions into a coordinated
workflow. An orchestrator — AWS Step Functions here — owns the sequence,
retries, branching, and state; each Lambda owns a single step.

## Files

- `order_stack.py` — CDK (Python) stack: five `LambdaInvoke` tasks wired
  into a state machine with a `Choice` branch. Payment failure routes to a
  refund compensation step, then `Fail`.
- `steps.py` — the five Lambda handlers (validate, pay, reserve, notify,
  refund). Each returns a dict the orchestrator feeds to the next state.
- `state_machine.asl.json` — the same workflow as an Amazon States Language
  definition, with a `Retry` block on the payment task (service exceptions
  only, exponential backoff).
- `start_execution.py` — starts an execution with a unique name and polls
  `describe_execution` for status, output, and error.

## Requirements

- Python 3.11+ with `boto3`; `aws-cdk-lib` and `constructs` for the stack.
- Deploy with `cdk deploy` (or create the state machine from
  `state_machine.asl.json` and point `FunctionName` at your functions).

## Usage

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

## Notes

- Keep every step idempotent: the orchestrator may retry a task.
- Step Functions caps state input/output at 256KB — pass references
  (S3 keys, IDs), not full payloads.
- Don't put `retry_on_failure` on the `StateMachine` construct — it isn't
  a valid prop. Retries belong on the tasks, or on ASL `Retry`/`Catch`.
