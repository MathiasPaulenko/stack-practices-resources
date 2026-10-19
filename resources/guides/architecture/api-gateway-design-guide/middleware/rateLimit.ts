import { json, Middleware } from '../pipeline/types';

export interface TokenBucketStore {
  get(key: string): Promise<{ tokens: number; lastRefill: number } | null>;
  set(key: string, tokens: number, lastRefill: number, ttlSeconds: number): Promise<void>;
}

interface RateLimitConfig {
  store: TokenBucketStore;
  keyPrefix: string;
  capacity: number;
  refillPerSecond: number;
  identify: (headers: Record<string, string>) => string;
  now?: () => number;
}

// Distributed counters are the whole point: swap the in-memory store for Redis
// and every replica enforces the same quota.
export function rateLimitMiddleware(config: RateLimitConfig): Middleware {
  const now = config.now ?? (() => Date.now());

  return async (req, next) => {
    const clientId = config.identify(req.headers);
    const key = `${config.keyPrefix}:${clientId}`;

    const state = (await config.store.get(key)) ?? {
      tokens: config.capacity,
      lastRefill: now(),
    };
    const tokens = Math.min(
      config.capacity,
      state.tokens + ((now() - state.lastRefill) / 1000) * config.refillPerSecond
    );

    if (tokens < 1) {
      await config.store.set(key, tokens, state.lastRefill, 60);
      const retryAfter = Math.ceil((1 - tokens) / config.refillPerSecond);
      return json(429, { error: 'Rate limit exceeded' }, { 'retry-after': String(retryAfter) });
    }

    await config.store.set(key, tokens - 1, now(), 60);
    const response = await next();
    response.headers['x-ratelimit-remaining'] = String(Math.floor(tokens - 1));
    return response;
  };
}
