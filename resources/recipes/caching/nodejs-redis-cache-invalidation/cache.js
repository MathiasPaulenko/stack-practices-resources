// Cache invalidation helpers from the StackPractices
// nodejs-redis-cache-invalidation recipe. The Redis client is injected so the
// same helpers run against ioredis (server.js) or ioredis-mock (test.js).
const DEFAULT_TTL = 300;
const INVALIDATION_CHANNEL = 'cache:invalidate';

// Cache-aside write with TTL — Redis auto-expires the key.
async function cacheProduct(redis, product, ttl = DEFAULT_TTL) {
  await redis.set(
    `product:${product.id}`,
    JSON.stringify(product),
    'EX', ttl
  );
}

async function getProduct(redis, id) {
  const data = await redis.get(`product:${id}`);
  return data ? JSON.parse(data) : null;
}

// Explicit deletion after a write, then repopulate with fresh data.
async function updateProduct(redis, productId, updates, db) {
  const product = await db.product.update(productId, updates);
  await redis.del(`product:${productId}`);
  await redis.set(`product:${productId}`, JSON.stringify(product), 'EX', DEFAULT_TTL);
  return product;
}

// Pattern-based clearing: SCAN (non-blocking) + pipelined DEL per batch.
async function invalidatePattern(redis, pattern) {
  const stream = redis.scanStream({ match: pattern, count: 100 });
  let deletedCount = 0;

  for await (const keys of stream) {
    const unique = [...new Set(keys)]; // SCAN may repeat keys across batches
    if (unique.length > 0) {
      const results = await redis.pipeline().del(...unique).exec();
      deletedCount += results.reduce((sum, [err, n]) => sum + (err ? 0 : n), 0);
    }
  }
  return deletedCount;
}

// Publish an invalidation event so other instances drop the key from
// their in-memory L1 caches.
async function publishInvalidation(redis, keys, type = 'delete') {
  const event = { type, keys, timestamp: Date.now() };
  if (type === 'pattern') event.prefix = keys;
  return redis.publish(INVALIDATION_CHANNEL, JSON.stringify(event));
}

// Subscriber side: keep an L1 Map in sync. Pub/sub is fire-and-forget —
// on reconnect the L1 cache is cleared to be safe.
function createInvalidationSubscriber(redisOptions, RedisClient, localCache) {
  const subscriber = new RedisClient(redisOptions);
  subscriber.subscribe(INVALIDATION_CHANNEL);
  subscriber.on('error', (err) => console.error('subscriber error:', err));
  subscriber.on('reconnecting', () => localCache.clear());

  subscriber.on('message', (channel, message) => {
    if (channel !== INVALIDATION_CHANNEL) return;
    const event = JSON.parse(message);
    if (event.type === 'delete') {
      event.keys.forEach((key) => localCache.delete(key));
    } else if (event.type === 'pattern') {
      for (const key of localCache.keys()) {
        if (key.startsWith(event.prefix)) localCache.delete(key);
      }
    } else if (event.type === 'flush') {
      localCache.clear();
    }
  });
  return subscriber;
}

// Cache-aside read with a stampede lock: only one requester fetches from
// the DB; the rest wait briefly, then fall back to a direct read.
async function getProductWithLock(redis, productId, db, retries = 5) {
  const cacheKey = `product:${productId}`;
  const lockKey = `lock:${cacheKey}`;

  const cached = await redis.get(cacheKey);
  if (cached) return JSON.parse(cached);

  const lockAcquired = await redis.set(lockKey, '1', 'NX', 'EX', 10);
  if (lockAcquired) {
    try {
      const product = await db.product.findById(productId);
      if (product) {
        await redis.set(cacheKey, JSON.stringify(product), 'EX', DEFAULT_TTL);
      }
      return product;
    } finally {
      await redis.del(lockKey);
    }
  }

  if (retries <= 0) return db.product.findById(productId);
  await new Promise((resolve) => setTimeout(resolve, 100 + Math.random() * 100));
  return getProductWithLock(redis, productId, db, retries - 1);
}

module.exports = {
  DEFAULT_TTL,
  INVALIDATION_CHANNEL,
  cacheProduct,
  getProduct,
  updateProduct,
  invalidatePattern,
  publishInvalidation,
  createInvalidationSubscriber,
  getProductWithLock,
};
