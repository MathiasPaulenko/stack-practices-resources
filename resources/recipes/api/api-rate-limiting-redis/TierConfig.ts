// rate-limiter/TierConfig.ts
// Per-user tier configuration: bucket capacity and refill rate
// keyed by subscription level.
import { Request, Response, NextFunction } from 'express';
import { TokenBucketLimiter } from './TokenBucket';

interface RateLimitConfig {
  capacity: number;
  refillRate: number;
}

const tierLimits: Record<string, RateLimitConfig> = {
  free: { capacity: 100, refillRate: 10 },
  pro: { capacity: 1000, refillRate: 100 },
  enterprise: { capacity: 10000, refillRate: 1000 },
};

async function getUserTier(userId: string): Promise<string> {
  // Fetch from database or cache
  return 'pro';
}

// Middleware with tier lookup
export function tieredRateLimit(limiter: TokenBucketLimiter) {
  return async (req: Request, res: Response, next: NextFunction) => {
    const userId = req.headers['x-user-id'] as string;
    const tier = userId ? await getUserTier(userId) : 'free';
    const config = tierLimits[tier] || tierLimits.free;

    const key = `${tier}:${userId || req.ip}`;
    const result = await limiter.check(key, config.capacity, config.refillRate);

    if (!result.allowed) {
      res.status(429).json({ error: 'Rate limit exceeded', tier });
      return;
    }

    next();
  };
}
