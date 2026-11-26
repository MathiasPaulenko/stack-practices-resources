# Serverless Event Sourcing Pattern

Companion code for the StackPractices pattern:
<https://stackpractices.com/patterns/serverless-event-sourcing-pattern/>

Event sourcing stores application state as an append-only log of immutable
events. On AWS, DynamoDB works as the event store, DynamoDB Streams drive the
projection Lambda, and EventBridge fans events out to downstream consumers.

## Files

- `event_store.py` — Python `EventStore` on DynamoDB: append with optimistic
  concurrency (conditional write on `aggregateId` + `version`), ordered
  queries, and replay to rebuild aggregate state.
- `projection_handler.py` — Lambda triggered by the table stream that
  projects state into `order_projection`, with idempotent upserts keyed on
  the incoming version.
- `event-store.ts` — TypeScript variant that also publishes each appended
  event to EventBridge for downstream consumers.
- `template.yaml` — SAM template with the `event_store` table (streams +
  PITR), the `order_projection` read model, and the projection function
  wired to the stream.

## Requirements

- Python 3.11+ with `boto3`, or Node.js 18+ with `@aws-sdk/client-dynamodb`,
  `@aws-sdk/client-eventbridge`, and `@aws-sdk/util-dynamodb`.
- AWS credentials with DynamoDB access. Deploy `template.yaml` with
  `sam deploy --guided` to create the tables and the projection function.

## Usage

```python
from event_store import create_order, confirm_order, get_order_state

create_order("order-1", "customer-42", [{"sku": "A1", "qty": 2}])
confirm_order("order-1")
print(get_order_state("order-1"))
# {'customerId': 'customer-42', 'items': [...], 'status': 'CONFIRMED', 'version': 2}
```

The projection function runs automatically on every stream INSERT — no
manual trigger needed once deployed.
