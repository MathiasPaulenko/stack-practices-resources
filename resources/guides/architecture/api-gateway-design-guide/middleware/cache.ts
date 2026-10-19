import { json, Middleware } from '../pipeline/types';

export interface ResponseCacheStore {
  get(key: string): Promise<{ status: number; body: unknown; headers: Record<string, string> } | null>;
  set(key: string, value: { status: number; body: unknown; headers: Record<string, string> }, ttlSeconds: number): Promise<void>;
}

// GET responses cached with the caller's identity in the key — without it,
// one user's data leaks to the next.
export function cacheMiddleware(cache: ResponseCacheStore, defaultTtl = 60): Middleware {
  return async (req, next) => {
    if (req.method !== 'GET') return next();

    const cacheKey = `${req.headers['x-user-id'] ?? 'anon'}:${req.path}:${JSON.stringify(req.query)}`;
    const cached = await cache.get(cacheKey);
    if (cached) {
      return { ...cached, headers: { ...cached.headers, 'x-cache': 'HIT' } };
    }

    const response = await next();
    if (response.status === 200) {
      const match = /max-age=(\d+)/.exec(response.headers['cache-control'] ?? '');
      const ttl = match ? parseInt(match[1], 10) : defaultTtl;
      await cache.set(cacheKey, response, ttl);
      response.headers['x-cache'] = 'MISS';
    }
    return response;
  };
}
