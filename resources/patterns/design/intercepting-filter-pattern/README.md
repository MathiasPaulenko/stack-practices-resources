# Intercepting Filter Pattern — Companion Resources

Runnable examples for the [Intercepting Filter pattern](https://stackpractices.com/patterns/intercepting-filter-pattern/) on StackPractices.

The pattern composes cross-cutting concerns (auth, logging, compression) into a chain of filters that intercept requests before the target handler — and responses on the way back. It's the mechanism behind Express middleware, Java servlet filters, and ASP.NET Core pipelines.

## Files

| File | What it shows |
|------|---------------|
| `filter_chain.py` | Filter chain in Python: auth short-circuit, logging on both legs, gzip postprocessing |
| `filter_chain.js` | The same chain in JavaScript, with an `execute()` entry point that resets the cursor between requests |
| `test_filter_chain.py` | pytest suite: 6 tests covering short-circuit, postprocessing, and chain reuse |
| `express_app.js` | The same filters as Express-style middleware (`req, res, next`) with a minimal middleware engine |
| `express_app.test.js` | `node:test` suite for the JS chain and the middleware pipeline |

## Run it

```bash
# Python demo + tests
python filter_chain.py
python -m pytest test_filter_chain.py -v

# JavaScript demo + tests (Node 18+)
node filter_chain.js
node --test express_app.test.js

# Express-style server
node express_app.js   # then curl http://localhost:3000/api/hello
```

## Key takeaways

- A filter that doesn't delegate = short-circuit (the 401 path never reaches the target).
- Code after `chain.doFilter()` / `next()` runs on the response leg — that's how compression and logging-on-exit work.
- The chain's cursor is state; `execute()` resets it so one chain instance can serve every request.
- In async pipelines, forgetting `await`/`next()` means response filters never run — the most common production bug in middleware.

CI: `.github/workflows/test.yml` runs both test suites on every change to this folder.
