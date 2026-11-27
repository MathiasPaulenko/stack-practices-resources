# Stream Processing Guide — Code Examples

Companion code for [Stream Processing: Event-Driven Data Pipelines](https://stackpractices.com/guides/stream-processing-guide/) on StackPractices.

## Files

| File | Description |
|---|---|
| `cloudevents_order_schema.json` | CloudEvents-compliant `order.placed` event example |
| `schema_validator.py` | JSON-Schema event validation (Python) |
| `OrderAnalyticsApp.java` | Kafka Streams app: filter, KTable enrich join, tumbling-window aggregation |
| `FraudDetectionJob.java` | Flink job with keyed state (`ValueState`/`ListState`) for amount-spike and velocity rules |
| `ExactlyOnceConfig.java` | Kafka + Flink exactly-once setup: idempotent producer, checkpointing, transactional sink |
