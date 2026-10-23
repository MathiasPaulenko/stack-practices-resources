# Event-Driven Serverless Functions — Companion

Runnable companion for the [Event-Driven Serverless Functions](https://stackpractices.com/recipes/event-driven-functions/) recipe on StackPractices.com.

## Files

| File | Type | Contents |
|------|------|----------|
| `handler.py` | Python | SQS-triggered Lambda with idempotency (DynamoDB conditional write) and `batchItemFailures` partial batch response |
| `template.yaml` | SAM | Full infrastructure: EventBridge rule fanning out to two Lambdas + SQS, DLQ with `redrivePolicy`, invoke permissions, idempotency table |
| `publisher.mjs` | JavaScript (ESM) | EventBridge `PutEvents` publisher with `eventId` for consumer deduplication; runnable as a script |

## Usage

```bash
sam deploy --guided            # deploy the stack
node publisher.mjs             # send a test OrderPlaced event
sam logs -n PaymentFunction    # watch the consumer fire
```

## Notes

- The EventBridge rule matches `source: order-service` + `detail-type: OrderPlaced` — `DetailType` is case-sensitive.
- `batchItemFailures` is the difference between retrying one bad message and replaying the whole batch.
- `maxReceiveCount: 3` sends poison messages to the DLQ after three failed receives.
