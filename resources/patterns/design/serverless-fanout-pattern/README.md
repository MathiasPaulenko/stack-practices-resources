# Serverless Fanout Pattern

Companion code for the StackPractices pattern:
<https://stackpractices.com/patterns/serverless-fanout-pattern/>

The fanout pattern broadcasts one event to every subscribed consumer through
an SNS topic. Each consumer gets its own SQS queue, so a slow or failing
consumer never blocks the others — and the producer never knows who is
listening.

## Files

- `producer.py` — publishes `OrderPlaced` events to the SNS topic with a
  `MessageAttributes` filter key, so subscribers can filter without parsing
  the body.
- `consumer.py` — Lambda handler that processes SQS batches, treating the
  record body as raw JSON (raw message delivery) and returning
  `batchItemFailures` so only failed records are retried.
- `template.yaml` — SAM template with the SNS topic, two SQS queues with
  DLQs and `maxReceiveCount: 3`, raw-delivery subscriptions (one with a
  filter policy, one without), and the consumer functions.

## Requirements

- Python 3.11+ with `boto3`.
- AWS credentials with SNS/SQS/Lambda access. Deploy with
  `sam deploy --guided` to create the topic, queues, DLQs, and functions.

## Usage

```python
from producer import publish_order_event

publish_order_event("order-123", "customer-42", 149.99)
# Every subscribed queue receives a copy; each consumer scales and fails
# independently. Messages that fail 3 times land in that queue's DLQ.
```

## Notes

- Delivery is at-least-once: make consumers idempotent.
- Set queue `VisibilityTimeout` to at least 6x the consumer timeout.
- Use `RawMessageDelivery` so consumers see the event JSON, not the SNS
  envelope — unless you need the envelope metadata.
