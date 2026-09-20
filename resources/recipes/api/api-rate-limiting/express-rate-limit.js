/**
 * express-rate-limit.js — sliding-window rate limiter middleware for Express + Redis.
 *
 * Mount before route handlers:
 *   const { rateLimit } = require('./express-rate-limit');
 *   app.use(rateLimit({ limit: 100, windowSec: 60 }));
 *
 * Behavior:
 *   - Key: API key (x-api-key header) → user id (req.user?.id) → client IP
 *   - Within limit: passes through, sets X-RateLimit-* headers
 *   - Over limit: 429 + application/problem+json + Retry-After
 *   - Redis down: fails open (allows) and logs — decide your policy, this is ours
 */

const { createClient } = require('redis');

const client = createClient({ url: process.env.REDIS_URL || 'redis://localhost:6379' });
client.connect().catch(console.error);

function clientKey(req) {
  return req.get('x-api-key') || req.user?.id || req.ip;
}

function rateLimit({ limit = 100, windowSec = 60 } = {}) {
  return async (req, res, next) => {
    const now = Date.now();
    const windowStart = now - windowSec * 1000;
    const key = `rate_limit:sw:${clientKey(req)}`;

    try {
      await client.zRemRangeByScore(key, 0, windowStart);
      const count = await client.zCard(key);

      if (count >= limit) {
        const oldest = await client.zRangeWithScores(key, 0, 0);
        const retryAfter = oldest.length
          ? Math.ceil((oldest[0].score + windowSec * 1000 - now) / 1000)
          : windowSec;

        return res
          .status(429)
          .set('Retry-After', String(Math.max(1, retryAfter)))
          .set('X-RateLimit-Limit', String(limit))
          .set('X-RateLimit-Remaining', '0')
          .type('application/problem+json')
          .json({
            type: 'https://api.example.com/errors/rate-limit-exceeded',
            title: 'Rate Limit Exceeded',
            status: 429,
            detail: `You have exceeded the limit of ${limit} requests per ${windowSec}s. Retry after ${retryAfter} seconds.`,
            instance: req.originalUrl,
            request_id: req.id,
          });
      }

      await client.zAdd(key, [{ score: now, value: `${now}:${req.id || ''}` }]);
      await client.expire(key, windowSec);

      res.set('X-RateLimit-Limit', String(limit));
      res.set('X-RateLimit-Remaining', String(limit - count - 1));
      return next();
    } catch (err) {
      // Fail open — a dead limiter must not take the API down with it
      console.error({ requestId: req.id, err }, 'rate limiter unavailable, failing open');
      return next();
    }
  };
}

module.exports = { rateLimit };
