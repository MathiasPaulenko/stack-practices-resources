// Cache-aside with Redis (Node.js, redis v4+)
// Usage: node cache-aside.js  (requires Redis on localhost:6379)
const redis = require('redis');

const client = redis.createClient();

// Fake database for the demo
const db = {
  users: {
    findById: async (id) => ({ id, name: `User ${id}`, email: `user${id}@example.com` }),
  },
};

async function getUser(userId) {
  const cacheKey = `user:${userId}`;

  const cached = await client.get(cacheKey);
  if (cached) {
    console.log('cache HIT');
    return JSON.parse(cached);
  }

  console.log('cache MISS — querying database');
  const user = await db.users.findById(userId);
  if (user) {
    await client.setEx(cacheKey, 3600, JSON.stringify(user)); // TTL 1 hour
  }
  return user;
}

(async () => {
  await client.connect();
  console.log(await getUser(42)); // MISS
  console.log(await getUser(42)); // HIT
  await client.quit();
})();
