// rate-limiter/TokenBucket.ts
// Atomic token bucket backed by a Redis Lua script.
// Time is read inside the script via Redis TIME so every app node
// measures elapsed time against the same clock.
import { Redis } from 'ioredis';

export class TokenBucketLimiter {
  private redis: Redis;

  constructor(redis: Redis) {
    this.redis = redis;
  }

  async check(
    key: string,
    capacity: number,
    refillRate: number
  ): Promise<{ allowed: boolean; remaining: number; resetTime: number }> {
    const bucketKey = `ratelimit:token:${key}`;

    const luaScript = `
      local bucket = redis.call('HMGET', KEYS[1], 'tokens', 'lastRefill')
      local capacity = tonumber(ARGV[1])
      local refillRate = tonumber(ARGV[2])
      local interval = tonumber(ARGV[3])
      local time = redis.call('TIME')
      local now = tonumber(time[1]) * 1000 + math.floor(tonumber(time[2]) / 1000)

      local tokens = tonumber(bucket[1]) or capacity
      local lastRefill = tonumber(bucket[2]) or now

      local elapsed = now - lastRefill
      local refill = math.floor(elapsed / interval) * refillRate
      tokens = math.min(capacity, tokens + refill)

      if tokens >= 1 then
        tokens = tokens - 1
        redis.call('HMSET', KEYS[1], 'tokens', tokens, 'lastRefill', now)
        redis.call('EXPIRE', KEYS[1], 3600)
        return {1, tokens, now + interval}
      else
        redis.call('HMSET', KEYS[1], 'tokens', tokens, 'lastRefill', lastRefill)
        redis.call('EXPIRE', KEYS[1], 3600)
        return {0, tokens, lastRefill + interval}
      end
    `;

    const result = await this.redis.eval(luaScript, 1, bucketKey, capacity, refillRate, 1000);
    const [allowed, remaining, resetTime] = result as [number, number, number];

    return {
      allowed: allowed === 1,
      remaining,
      resetTime,
    };
  }
}
