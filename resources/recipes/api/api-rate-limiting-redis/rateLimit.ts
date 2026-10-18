// middleware/rateLimit.ts
// Express middleware that emits IETF RateLimit-* headers and
// returns 429 + Retry-After when the bucket is empty.
import { Request, Response, NextFunction } from 'express';
import { TokenBucketLimiter } from './TokenBucket';

export function rateLimit(
  limiter: TokenBucketLimiter,
  options: { capacity: number; refillRate: number }
) {
  return async (req: Request, res: Response, next: NextFunction) => {
    const key = `${req.ip}:${req.route?.path || req.path}`;
    const result = await limiter.check(key, options.capacity, options.refillRate);

    res.setHeader('RateLimit-Limit', String(options.capacity));
    res.setHeader('RateLimit-Remaining', String(Math.max(0, result.remaining)));
    res.setHeader('RateLimit-Reset', String(Math.ceil(result.resetTime / 1000)));

    if (!result.allowed) {
      res.setHeader('Retry-After', String(Math.ceil((result.resetTime - Date.now()) / 1000)));
      res.status(429).json({
        error: 'Too Many Requests',
        retryAfter: Math.ceil((result.resetTime - Date.now()) / 1000),
      });
      return;
    }

    next();
  };
}
