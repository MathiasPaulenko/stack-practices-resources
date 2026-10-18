// rate-limiter/SlidingWindow.ts
// Sliding window counter backed by a Redis sorted set.
// pipeline.exec() returns [err, result] tuples — index 1 holds the ZCARD count.
import { Redis } from 'ioredis';

export class SlidingWindowLimiter {
  private redis: Redis;

  constructor(redis: Redis) {
    this.redis = redis;
  }

  async check(
    key: string,
    limit: number,
    windowMs: number
  ): Promise<{ allowed: boolean; remaining: number; resetTime: number }> {
    const now = Date.now();
    const windowKey = `ratelimit:window:${key}`;
    const windowStart = now - windowMs;

    const pipeline = this.redis.pipeline();
    pipeline.zremrangebyscore(windowKey, 0, windowStart);
    pipeline.zcard(windowKey);
    pipeline.zadd(windowKey, now, `${now}-${Math.random()}`);
    pipeline.pexpire(windowKey, windowMs);

    const results = await pipeline.exec();
    const currentCount = (results?.[1]?.[1] ?? 0) as number;

    if (currentCount < limit) {
      return {
        allowed: true,
        remaining: limit - currentCount - 1,
        resetTime: now + windowMs,
      };
    }

    // Remove the request we just added
    await this.redis.zremrangebyrank(windowKey, -1, -1);

    const oldest = await this.redis.zrange(windowKey, 0, 0, 'WITHSCORES');
    const resetTime = oldest.length > 0 ? Number(oldest[1]) + windowMs : now + windowMs;

    return {
      allowed: false,
      remaining: 0,
      resetTime,
    };
  }
}
