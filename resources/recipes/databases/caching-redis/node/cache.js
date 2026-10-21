// Cache-aside + rate limiter (ioredis) from the StackPractices Redis caching recipe.

const Redis = require("ioredis");
const redis = new Redis({ host: "localhost", port: 6379 });

async function getCached(key, fetcher, ttl = 300) {
  const cached = await redis.get(key);
  if (cached) return JSON.parse(cached);

  const data = await fetcher();
  await redis.setex(key, ttl, JSON.stringify(data));
  return data;
}

async function getUser(userId) {
  return getCached(
    `user:${userId}`,
    async () => {
      // Expensive DB query
      return { id: userId, name: "Alice", orders: 42 };
    },
    600
  );
}

// Invalidate cache
async function invalidateUser(userId) {
  await redis.del(`user:${userId}`);
}

// Redis as rate limiter
async function rateLimit(key, maxRequests = 100, window = 60) {
  const current = await redis.incr(key);
  if (current === 1) await redis.expire(key, window);
  return current <= maxRequests;
}

module.exports = { getCached, getUser, invalidateUser, rateLimit };

if (require.main === module) {
  (async () => {
    console.log(await getUser(1));
    await invalidateUser(1);
    console.log(await rateLimit("rl:demo"));
    redis.disconnect();
  })();
}
