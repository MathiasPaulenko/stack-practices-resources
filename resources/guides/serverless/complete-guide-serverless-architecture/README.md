# Serverless Image Processing Pipeline

Companion code for the [Complete Guide to Serverless Architecture](https://stackpractices.com/guides/complete-guide-serverless-architecture/) — the worked example: an event-driven pipeline `S3 upload → resize Lambda → SQS → metadata Lambda → DynamoDB` with a dead-letter queue.

## Files

| File | Purpose |
|------|---------|
| `resize_handler.py` | S3-triggered Lambda: resizes the uploaded image (thumbnail/medium/large) and publishes the generated keys to SQS |
| `metadata_handler.py` | SQS-triggered Lambda: writes per-version metadata to DynamoDB; returns `batchItemFailures` so only failed messages retry |
| `main.tf` | Terraform for both Lambdas, the SQS queue + DLQ, the event source mapping, and the DynamoDB table |
| `requirements.txt` | Python dependencies (`boto3`, `Pillow`) |

## Run locally

The handlers are plain functions — invoke them with a mocked event:

```bash
pip install -r requirements.txt

python - <<'PY'
import json
import metadata_handler

event = {"Records": [{"messageId": "m1", "body": json.dumps({
    "imageId": "img-1",
    "originalKey": "uploads/originals/photo.jpg",
    "thumbnailKey": "uploads/resized/t.jpg",
    "mediumKey": "uploads/resized/m.jpg",
    "largeKey": "uploads/resized/l.jpg",
})}]}
print(metadata_handler.lambda_handler(event, None))
PY
```

`metadata_handler` runs without AWS credentials when `TABLE_NAME` is set and `boto3` is mocked or pointed at LocalStack. `resize_handler` needs S3 access (real or LocalStack) and Pillow.

## Deploy

```bash
terraform init
terraform apply
```

Then package each handler (`zip` + `lambda update-function-code`) or deploy with SAM / Serverless Framework.
