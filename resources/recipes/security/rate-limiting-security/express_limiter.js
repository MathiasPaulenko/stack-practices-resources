// Tiered rate limiting middleware for Express using rate-limiter-flexible.
// Requires: npm install rate-limiter-flexible redis
const { RateLimiterRedis } = require('rate-limiter-flexible');
const redis = require('redis');

const redisClient = redis
  .createClient({ url: process.env.REDIS_URL });

// Auth endpoints: 5 attempts/min, then block for 5 minutes
const authLimiter = new RateLimiterRedis({
  storeClient: redisClient,
  keyPrefix: 'auth',
  points: 5,
  duration: 60,
  blockDuration: 300,
});

// General API: 100 requests per 10 seconds
const apiLimiter = new RateLimiterRedis({
  storeClient: redisClient,
  keyPrefix: 'api',
  points: 100,
  duration: 10,
});

function createLimiter(limiter, keyFn = (req) => req.ip) {
  return async (req, res, next) => {
    try {
      await limiter.consume(keyFn(req), 1);
      next();
    } catch (rej) {
      const retryAfter = Math.ceil(rej.msBeforeNext / 1000);
      res.set('Retry-After', String(retryAfter));
      res.set('X-RateLimit-Remaining', '0');
      res.status(429).json({ error: 'Too many requests', retryAfter });
    }
  };
}

module.exports = function attachLimiters(app) {
  app.use('/api/', createLimiter(apiLimiter));
  // Key on IP + credential: stops stuffing one source across many accounts
  app.use(
    '/api/auth/',
    createLimiter(authLimiter, (req) => `${req.ip}:${req.body?.email || ''}`)
  );
};
