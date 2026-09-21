// Fixed-window rate limiter with Redis — works across app instances.
// Requires: npm install redis && a reachable Redis (redis://localhost:6379).
const redis = require('redis');
const client = redis.createClient();

async function rateLimit(key, limit, windowSeconds) {
  const windowKey = `${key}:${Math.floor(Date.now() / 1000 / windowSeconds)}`;
  const current = await client.incr(windowKey);
  if (current === 1) {
    await client.expire(windowKey, windowSeconds);
  }
  return current <= limit;
}

// Express middleware — 100 req/min per IP by default
async function limiter(req, res, next) {
  const key = `ratelimit:${req.ip}`;
  const allowed = await rateLimit(key, 100, 60);
  if (!allowed) {
    res.set('Retry-After', '60');
    return res.status(429).json({ error: 'Too many requests' });
  }
  next();
}

// Per-endpoint budgets: tighten the routes attackers actually hammer.
const LIMITS = {
  'POST:/login': { limit: 5, window: 60 },
  'POST:/reports/export': { limit: 10, window: 3600 },
  default: { limit: 100, window: 60 },
};

async function perEndpointLimiter(req, res, next) {
  const cfg = LIMITS[`${req.method}:${req.route?.path}`] ?? LIMITS.default;
  const key = `ratelimit:${req.user?.id ?? req.ip}:${req.method}:${req.route?.path}`;
  const allowed = await rateLimit(key, cfg.limit, cfg.window);
  if (!allowed) {
    res.set('Retry-After', String(cfg.window));
    return res.status(429).json({ error: 'Too many requests' });
  }
  next();
}

module.exports = { rateLimit, limiter, perEndpointLimiter };
