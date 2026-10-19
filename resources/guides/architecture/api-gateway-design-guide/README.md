# API Gateway Design — Middleware Pipeline Example

Runnable TypeScript example for the [API Gateway design guide](https://stackpractices.com/guides/api-gateway-design-guide/) on StackPractices.

A minimal gateway pipeline that composes the four middleware layers from the guide — authentication, rate limiting, response caching, and circuit breaking — in front of a stateless prefix router. No Express, no Redis, no JWT library: framework-agnostic types plus `node:crypto` for HS256 verification.

## Structure

```text
pipeline/        types.ts (Request/Response/Middleware) + gateway.ts (composition)
middleware/      auth.ts (JWT + identity headers)
                 rateLimit.ts (token bucket, pluggable store)
                 cache.ts (GET cache with per-user keys)
                 circuitBreaker.ts (closed/open/half-open)
routing/         router.ts (prefix routing, optional stripPrefix)
stores/          InMemoryTokenBucketStore, InMemoryResponseCache
upstream/        StubUpstream (scriptable test double)
tests/           Jest tests covering the full pipeline
```

## How it works

`createGateway(middlewares, router)` reduces the middleware list over the router so `auth → rateLimit → cache → circuitBreaker → router` runs in order — the same sequence the guide's pipeline diagram shows (TLS termination aside, which lives at the load balancer).

1. `authMiddleware` verifies the JWT, injects `x-user-id`/`x-user-roles`/`x-user-scopes` for upstreams, and short-circuits with 401.
2. `rateLimitMiddleware` refills a token bucket keyed by identity through a `TokenBucketStore` — swap `InMemoryTokenBucketStore` for a Redis implementation and every replica shares the quota.
3. `cacheMiddleware` caches GET responses with the caller's identity in the key and honors upstream `Cache-Control: max-age`.
4. `circuitBreakerMiddleware` fails fast after N consecutive upstream errors, then lets a limited number of probes through while half-open.
5. `createRouter` matches by prefix; `stripPrefix` rewrites `/api/users/42` to `/42` before forwarding.

## Running the tests

The suites need no external services — all stores are in-memory and the upstream is a scriptable stub:

```bash
npm install -D typescript ts-jest @types/jest jest
npx jest tests/
```

## Wiring it for real

Replace the in-memory pieces at the composition root: a Redis-backed `TokenBucketStore`, your framework's adapter translating HTTP into `GatewayRequest`, and real `Upstream` functions per route. The middleware contracts stay identical — that's the point of keeping them framework-agnostic.
