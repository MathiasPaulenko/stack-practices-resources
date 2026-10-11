# Event Sourcing in Serverless Architectures — Companion Code

TypeScript reference implementation of the three pieces from the
[event-sourcing-serverless recipe](https://stackpractices.com/recipes/event-sourcing-serverless/)
on StackPractices.com:

- `sourcing/eventstore.ts` — append-only event store on DynamoDB with per-aggregate
  versioning and optimistic concurrency (`ConditionExpression`).
- `sourcing/projection.ts` — Lambda handler triggered by a DynamoDB Stream that routes
  each appended event to the right read-model projection. Includes a note on
  idempotency (streams are at-least-once).
- `sourcing/aggregate.ts` — order aggregate rebuilt by replaying its event history,
  with `toSnapshot()` for snapshot-based loads.
- `sourcing/eventstore.py` — the same event store in Python/boto3
  (`transact_write_items` + `TypeSerializer`).

## Dependencies

```bash
npm install @aws-sdk/client-dynamodb @aws-sdk/lib-dynamodb @aws-sdk/util-dynamodb
npm install -D @types/aws-lambda
```

## Notes

- The projection writers in `projection.ts` are stubs — implement them against
  your read-model store (another DynamoDB table, RDS, OpenSearch...).
- The event store key layout is `PK = ORDER#<id>`, `SK = EVENT#<padded version>`.
  Enable a DynamoDB Stream (`NEW_IMAGE`) on the table to feed the projection Lambda.
- For aggregates with long histories, snapshot every 50–100 events under a separate
  key (`SK = SNAPSHOT#<version>`) and replay only newer events.
