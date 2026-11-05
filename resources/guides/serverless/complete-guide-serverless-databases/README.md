# Complete Guide to Serverless Databases — Companion Examples

Companion for [Complete Guide to Serverless Databases](https://stackpractices.com/guides/complete-guide-serverless-databases/).

- `dynamodb_example.js` — order service with access-pattern-first key design (Query on partition key, no Scan).
- `lambda_warm_connection.js` — the warm-connection reuse pattern: initialize the pg client outside the Lambda handler.
