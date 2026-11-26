# API Gateway Lambda Authorizers — Companion Resources

Runnable authorizer examples matching the [Secure API Gateway with Custom Lambda Authorizers](https://stackpractices.com/recipes/serverless-api-gateway-lambda-authorizer/) recipe.

## Contents

| File | Purpose |
|------|---------|
| `src/authorizer.py` | JWT authorizer — validates Bearer token, returns IAM policy + context |
| `src/authorizer_rbac.py` | Role-based variant — admin/editor/user method permissions |
| `src/authorizer_apikey.py` | API-key authorizer with DynamoDB lookup (hashed keys) |
| `template.yaml` | SAM template: authorizer + protected resource + 300s result cache |

## Usage

```bash
# requires PyJWT in src/ or a Lambda layer
sam build && sam deploy --guided

# test locally
sam local invoke AuthFunction --event event.json
```

Se
