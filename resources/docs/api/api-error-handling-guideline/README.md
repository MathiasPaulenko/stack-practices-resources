# API Error Handling Guideline — Companion Resources

Companion files for the [API Error Handling Guideline](https://stackpractices.com/docs/api-error-handling-guideline/) on StackPractices.com.

## What's included

| File | Description |
|------|-------------|
| `error-handler-express.js` | Central Express.js error handler + `ApiError` class (ready to wire with `app.use`) |
| `error-handler-flask.py` | Flask `ApiError` exception + `@app.errorhandler` implementation |
| `error-registry.json` | Machine-readable error code registry — statuses, retryable flags, descriptions |
| `api-client-error.js` | Typed client-side error consumer honoring `Retry-After` |

## Quick start

1. Drop the handler matching your stack into your project and register it after your routes.
2. Import `error-registry.json` wherever errors are created — codes are constants, not strings.
3. Extend the registry with domain codes; retire codes with `deprecated: true`, never delete.
