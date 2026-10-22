// Cache stampede protection with a Redis lock (SET NX EX)
// Only one request rebuilds the value; others poll until the cache is populated.
const redis = require('redis');

const client = redis.createClient();

async function getWithLock(key, ttl, builder) {
  const cached = await client.get(key);
  if (cached) return JSON.parse(cached);

  const lockKey = `${key}:lock`;
  const acquired = await client.set(lockKey, '1', { NX: true, EX: 10 });

  if (!acquired) {
    // Someone else is rebuilding — wait briefly and retry
    await new Promise((resolve) => setTimeout(resolve, 100));
    return getWithLock(key, ttl, builder);
  }

  try {
    const value = await builder();
    await client.setEx(key, ttl, JSON.stringify(value));
    return value;
  } finally {
    await client.del(lockKey);
  }
}

(async () => {
  await client.connect();

  const expensiveQuery = async () => {
    console.log('rebuilding from the database…');
    await new Promise((r) => setTimeout(r, 300));
    return { total: 12345 };
  };

  // Simulate 5 concurrent requests on a cold cache — only one rebuilds
  const results = await Promise.all(
    Array.from({ length: 5 }, () => getWithLock('stats:daily', 300, expensiveQuery))
  );
  console.log(results);
  await client.quit();
})();
