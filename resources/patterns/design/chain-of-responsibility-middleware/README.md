# Chain of Responsibility — Middleware Pipeline

Runnable companion code for the StackPractices pattern
[Chain of Responsibility for Request Processing Middleware](https://stackpractices.com/patterns/chain-of-responsibility-middleware/).

Both implementations simulate an HTTP request crossing
auth → rate limit → validation → logging before it reaches the endpoint
handler. Any link can short-circuit the chain — an invalid token returns 401
without touching the rest of the pipeline.

## Files

| File | What it shows |
| --- | --- |
| `src/middleware-chain.js` | Class-based handler chain (`MiddlewareHandler`, `setNext`, `canHandle`, `process`). Runs three demo requests: a passing POST, a rejected request without token, and a GET that skips validation. |
| `src/express-compose.js` | Express/Koa-style `compose()`: the same `dispatch(i)` loop `koa-compose` uses, including the double-`next()` guard. |
| `src/middleware-chain.ts` | Typed TypeScript version of the class-based chain. |
| `src/AuthFilter.java` | Java Servlet API variant: `FilterChain.doFilter()` is the pattern's `next()`; skipping it short-circuits the chain. |

## Usage

```bash
node src/middleware-chain.js   # class-based chain demo
node src/express-compose.js    # compose() dispatch demo
npx tsx src/middleware-chain.ts  # TypeScript version (needs tsx or ts-node)
```

Expected output for the first file:

```text
Request 1: authenticated POST (passes every link)
  auth        -> user user123
  rate limit  -> 1/100 for cli-1
  validation  -> body ok
  logging     -> ... POST /orders
  endpoint    -> 200 OK for /orders

Request 2: missing token (auth short-circuits)
  chain error -> 401 Unauthorized

Request 3: GET skips validation but crosses auth/rate-limit/logging
  auth        -> user user123
  rate limit  -> 1/100 for user123
  logging     -> ... GET /orders
  endpoint    -> 200 OK for /orders
```

Note the rate limiter counts `cli-1` for request 1 and `user123` for
request 3 — the auth link has already set `req.user.id` by then, which is
the client ID fallback order (`x-client-id` → `req.user.id` → `anonymous`)
the article describes.

## Related

- Pattern page (EN): <https://stackpractices.com/patterns/chain-of-responsibility-middleware/>
- Pattern page (ES): <https://stackpractices.com/es/patterns/chain-of-responsibility-middleware/>
- Generic pattern: <https://stackpractices.com/patterns/chain-of-responsibility-pattern/>
