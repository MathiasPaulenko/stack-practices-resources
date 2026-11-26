# Event-Driven Lambda with SQS Triggers — Companion Files

Runnable companion for the [SQS-triggered Lambda recipe](https://stackpractices.com/recipes/serverless-event-driven-sqs-lambda/) on StackPractices.

- `lambda_function.py` — batch consumer with partial batch responses (`batchItemFailures`) so only failed messages return to the queue.
- `producer.py` — single sends, `send_message_batch` (batches of 10) and FIFO ordered sends with message groups and deduplication IDs.
- `template.yaml` — SAM template: main queue + DLQ with redrive policy, SQS trigger with `BatchSize`/`MaxBatchingWindow`/`ReportBatchItemFailures`, SNS alert topic and a CloudWatch alarm on DLQ depth.
- `queue-attributes.json` — CLI attributes file for `aws sqs create-queue` (replace `<DLQ_ARN>` with your dead-letter queue ARN).
- `drain_queue.py` — scheduled handler that polls and drains a queue when invoked by an EventBridge rule.

Requires `boto3`, AWS credentials, and `sam` for the template.
