# Mock Server Pattern — Companion Code

Runnable, dependency-free implementations of the [Mock Server Pattern](https://stackpractices.com/patterns/mock-server-pattern/): a real HTTP server on a local port that returns canned responses, records every request, and lets tests verify calls afterwards.

Both files implement the same four-step lifecycle used by WireMock, nock, MSW, and Mountebank:

1. **Configure** — `stub(method, path, status, body)` registers a canned response.
2. **Intercept** — the code under test fires a real HTTP request to a real socket.
3. **Match and respond** — the first stub whose method + path match wins; unmatched paths 404.
4. **Verify** — `verify(method, path)` confirms the request actually arrived.

## Files

| File | Stack | Tests |
|------|-------|-------|
| `mock_server.py` | Python stdlib (`http.server`, `threading`, `urllib`) | 5 unittest cases |
| `mock_server.mjs` | Node.js (`node:http`, `node:test`, `fetch`) | 5 cases under `node --test` |

## Run

```bash
# Python — demo + test suite
python mock_server.py
python -m unittest mock_server -v

# Node — tests only (the file also runs a demo when executed directly)
node --test mock_server.mjs
node mock_server.mjs
```

## What the tests cover

- A stubbed response reaches the client over a real socket.
- Stubbed error statuses (404) propagate to client exceptions.
- Unstubbed paths 404 by default — the no-match behavior is itself testable.
- `verify()` distinguishes "the request happened" from "the test passed".
- `reset()` between tests prevents leaked stubs — the top cause of ghost failures in real suites.

## When to use a real mock server vs. an interceptor

A real port (like these) exercises your HTTP client's socket behavior — timeouts, retries, TLS. In-process interceptors like nock or `responses` are faster and can't have port collisions, which is why they're the usual pick in CI. The [pattern page](https://stackpractices.com/patterns/mock-server-pattern/) has the full decision table.
