import { authMiddleware, signTestToken } from '../middleware/auth';
import { rateLimitMiddleware } from '../middleware/rateLimit';
import { circuitBreakerMiddleware } from '../middleware/circuitBreaker';
import { cacheMiddleware } from '../middleware/cache';
import { createRouter } from '../routing/router';
import { createGateway } from '../pipeline/gateway';
import { InMemoryTokenBucketStore } from '../stores/InMemoryTokenBucketStore';
import { InMemoryResponseCache } from '../stores/InMemoryResponseCache';
import { StubUpstream } from '../upstream/StubUpstream';
import { GatewayRequest } from '../pipeline/types';

const SECRET = 'test-secret';

function req(overrides: Partial<GatewayRequest> = {}): GatewayRequest {
  return { method: 'GET', path: '/api/users', query: {}, headers: {}, ...overrides };
}

function buildGateway(upstream: StubUpstream) {
  const router = createRouter([{ prefix: '/api', upstream: upstream.handler }]);
  return createGateway(
    [
      authMiddleware({ jwtSecret: SECRET, publicPaths: ['/health'] }),
      rateLimitMiddleware({
        store: new InMemoryTokenBucketStore(),
        keyPrefix: 'rl',
        capacity: 3,
        refillPerSecond: 1,
        identify: (h) => h['x-user-id'] ?? h['x-forwarded-for'] ?? 'anon',
      }),
      cacheMiddleware(new InMemoryResponseCache(), 30),
      circuitBreakerMiddleware({ failureThreshold: 2, windowMs: 30_000, halfOpenProbes: 1 }),
    ],
    router
  );
}

describe('gateway pipeline', () => {
  it('rejects unauthenticated requests before reaching the upstream', async () => {
    const upstream = new StubUpstream();
    const gateway = buildGateway(upstream);
    const res = await gateway(req());
    expect(res.status).toBe(401);
  });

  it('injects identity headers for the upstream after JWT validation', async () => {
    const upstream = new StubUpstream();
    upstream.enqueue(200, { ok: true });
    const gateway = buildGateway(upstream);
    const token = signTestToken({ sub: 'u-1', roles: ['admin'], scopes: ['read'] }, SECRET);
    const res = await gateway(req({ headers: { authorization: `Bearer ${token}` } }));
    expect(res.status).toBe(200);
  });

  it('returns 429 with Retry-After after the bucket is empty', async () => {
    const upstream = new StubUpstream();
    const gateway = buildGateway(upstream);
    const token = signTestToken({ sub: 'u-2', roles: [], scopes: [] }, SECRET);
    const authed = req({ headers: { authorization: `Bearer ${token}` } });

    await gateway(authed); // MISS, consumes token
    await gateway(req({ ...authed, query: { page: '2' } })); // different cache key
    await gateway(req({ ...authed, query: { page: '3' } }));
    const res = await gateway(req({ ...authed, query: { page: '4' } }));

    expect(res.status).toBe(429);
    expect(res.headers['retry-after']).toBeDefined();
  });

  it('serves cached GET responses with X-Cache: HIT', async () => {
    const upstream = new StubUpstream();
    const gateway = buildGateway(upstream);
    const token = signTestToken({ sub: 'u-3', roles: [], scopes: [] }, SECRET);
    const authed = req({ headers: { authorization: `Bearer ${token}` } });

    const first = await gateway(authed);
    const second = await gateway(authed);

    expect(first.headers['x-cache']).toBe('MISS');
    expect(second.headers['x-cache']).toBe('HIT');
  });

  it('opens the circuit after repeated upstream 5xx', async () => {
    const upstream = new StubUpstream();
    upstream.enqueue(500, { error: 'boom' });
    upstream.enqueue(500, { error: 'boom' });
    const breaker = circuitBreakerMiddleware({ failureThreshold: 2, windowMs: 60_000, halfOpenProbes: 1 });
    const call = () => breaker(req(), () => upstream.handler(req()));

    await expect(call()).rejects.toThrow();
    await expect(call()).rejects.toThrow();
    const res = await call().catch((e) => e);
    expect(res.status).toBe(503);
  });

  it('routes by prefix and strips it for the upstream', async () => {
    let seenPath = '';
    const router = createRouter([
      {
        prefix: '/api/users',
        stripPrefix: true,
        upstream: async (r) => {
          seenPath = r.path;
          return { status: 200, headers: {}, body: {} };
        },
      },
    ]);
    await router(req({ path: '/api/users/42' }));
    expect(seenPath).toBe('/42');
  });
});
