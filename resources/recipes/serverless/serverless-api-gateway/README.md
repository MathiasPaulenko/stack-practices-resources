# Serverless API Gateway — Companion Resources

Runnable files for the [Build Serverless APIs with API Gateway](https://stackpractices.com/recipes/serverless-api-gateway/) recipe on StackPractices.

## Files

| File | What it is |
|------|------------|
| `handler.py` | Python Lambda handler with GET/POST routing on `/users` using the API Gateway proxy event shape. |
| `handler.js` | Node.js equivalent, including the JSON body guard that turns malformed input into a 400 instead of a 502. |
| `main.tf` | Complete Terraform for a working API: IAM role, `AWS_PROXY` integration, `aws_lambda_permission`, deployment with `prod` stage, and the `invoke_url` output. |

## Usage

1. Zip the handler you want (`zip function.zip handler.js` or `handler.py` renamed to `index.py` / `index.js` as needed by `handler`).
2. `terraform init && terraform apply` in a folder containing `main.tf` and `function.zip`.
3. Hit the `invoke_url` output with `curl` — `GET /users` should return the JSON array.

If the endpoint returns `500 Internal Server Error`, check `aws lambda get-policy` — API Gateway needs `aws_lambda_permission` to invoke the function.
