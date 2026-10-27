// Token bucket on Redis + Express middleware returning 429 + headers
const redis = require("redis");

const TIERS = {
  free: { capacity: 10, refillRate: 60, refillIntervalSec: 60 },
  starter: { capacity: 50, refillRate: 300, refillIntervalSec: 60 },
  pro: { capacity: 200, refillRate: 1000, refillIntervalSec: 60 },
  enterprise: { capacity: 2000, refillRate: 10000, refillIntervalSec: 60 },
};

async function rateLimit(redisClient, key, options) {
  const { capacity, refillIntervalSec } = options;
  const now = Date.now();
  const bucketKey = `ratelimit:${key}`;
  // NOTE: illustrative pipeline — not atomic across instances.
  // In production, run the same logic as a Lua EVAL script on Redis.
  const result = await redisClient
    .multi()
    .hGetAll(bucketKey)
    .hSet(bucketKey, { tokens: capacity, lastRefill: now })
    .expire(bucketKey, refillIntervalSec * 2)
    .exec();

  const bucket = result[0];
  let tokens = parseFloat(bucket.tokens) || capacity;
  const lastRefill = parseInt(bucket.lastRefill) || now;
  const elapsed = (now - lastRefill) / 1000;
  tokens = Math.min(capacity, tokens + elapsed * (capacity / refillIntervalSec));

  if (tokens >= 1) {
    tokens -= 1;
    await redisClient.hSet(bucketKey, { tokens: tokens.toString(), lastRefill: now.toString() });
    return { allowed: true, remaining: Math.floor(tokens) };
  }
  const retryAfter = Math.ceil((1 - tokens) / (capacity / refillIntervalSec));
  await redisClient.hSet(bucketKey, { tokens: tokens.toString(), lastRefill: now.toString() });
  return { allowed: false, remaining: 0, retryAfter };
}

async function rateLimitMiddleware(req, res, next) {
  const apiKey = req.headers["x-api-key"];
  const tier = await getTierForApiKey(apiKey);
  const options = TIERS[tier] || TIERS.free;
  const result = await rateLimit(redisClient, apiKey, options);

  res.setHeader("X-RateLimit-Limit", options.refillRate);
  res.setHeader("X-RateLimit-Remaining", result.remaining);
  res.setHeader("X-RateLimit-Policy", `${tier};w=${options.refillIntervalSec}`);

  if (!result.allowed) {
    res.setHeader("Retry-After", result.retryAfter);
    return res.status(429).json({
      error: {
        code: "RATE_LIMIT_EXCEEDED",
        message: "Rate limit exceeded. Retry after the specified delay.",
        retryAfter: result.retryAfter,
      },
    });
  }
  next();
}
