# Build Serverless Functions — Companion

Runnable examples matching the recipe, testable locally without a cloud account.

Source article: [Build Serverless Functions](https://stackpractices.com/recipes/serverless-functions/)

## Structure

| Path | What it is |
|------|------------|
| `lambda/handler.py` | AWS Lambda handler — runs locally, prints the response |
| `lambda/event-api-gateway.json` | API Gateway proxy event for `sam local invoke` |
| `gcf/index.js` | Google Cloud Functions HTTP function |
| `sam/template.yaml` | SAM template for an S3-triggered function |
| `sam/events/s3-upload.json` | Sample S3 ObjectCreated event |
| `python/event_processor.py` | The S3→SNS record loop with fake clients — verifiable offline |

## Quick start

**Lambda handler (no AWS):** `python lambda/handler.py` — prints `{"message": "Hello, Mathias!"}`.

**Event processor (no AWS):** `python python/event_processor.py` — runs the record loop against fakes and asserts `processed=2`.

**GCF:** `cd gcf && npm install && npm start`, then `curl "http://localhost:8080/?name=Mathias"`.

**SAM:** `sam local invoke ProcessUpload --event sam/events/s3-upload.json` (requires AWS SAM CLI + Docker).

## Notes

- Cold start tip: clients created *outside* the handler (`boto3.resource` at module level) are reused on warm invocations.
- Event sources are at-least-once — design handlers idempotent; `event_processor.py` publishes a summary that is safe to re-emit.
