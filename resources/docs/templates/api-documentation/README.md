# API Documentation Template — Companion Resources

Companion files for the [API Documentation Template](https://stackpractices.com/docs/api-documentation/) on StackPractices.com.

## What's included

| File | Description |
|------|-------------|
| `api-documentation-template.md` | The fill-in-ready Markdown template — copy it into your repo and replace the `[bracketed]` placeholders |
| `openapi-fragment.yaml` | Matching OpenAPI 3.1 fragment for the GET/POST `[resource]` endpoints, the error envelope, and bearer auth |

## Quick start

1. Copy `api-documentation-template.md` into `docs/api/` in your repo.
2. Replace `[resource]`, `[Service Name]` and `api.example.com` with your values.
3. Drop `openapi-fragment.yaml` into your spec, extend it per endpoint, and lint it in CI (`spectral lint`).
