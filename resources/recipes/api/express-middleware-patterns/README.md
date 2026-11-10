# Express Middleware Composition Patterns

A dependency-free demo of the five composition patterns from the recipe, implemented on `node:http` so it runs anywhere — no `npm install` needed. The middleware model mirrors Express's `(req, res, next)` contract, so the code ports directly.

## Files

| File | What it shows |
|------|---------------|
| `middleware_pipeline.js` | `compose()` flattening middleware stacks, `asyncHandler()` forwarding rejections, `AsyncLocalStorage` request context with trace IDs, a unified error handler, and a tiny schema validator — all wired into a working `node:http` server |
| `pipeline.test.js` | `node:test` + `fetch` driving the real pipeline: happy path, validation failure (400), `AppError` mapping (403), and unhandled rejection capture (500) with trace ID propagation |

## Run

```bash
node middleware_pipeline.js   # starts the server on :3000
node --test pipeline.test.js  # runs the integration suite
```

Try it:

```bash
curl -i http://localhost:3000/users/1
curl -i -X POST http://localhost:3000/users -d '{"name": 42}'
curl -i -H "X-Trace-Id: my-trace" http://localhost:3000/users/1  # trace echoed back
```

Source: https://stackpractices.com/recipes/express-middleware-patterns/
