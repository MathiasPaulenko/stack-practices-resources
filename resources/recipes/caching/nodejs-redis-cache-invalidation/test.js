// E2E test for the invalidation helpers using ioredis-mock — no real Redis
// needed. Run with: npm test
const { test, beforeEach } = require('node:test');
const assert = require('node:assert');
const Redis = require('ioredis-mock');
const {
  cacheProduct,
  getProduct,
  updateProduct,
  invalidatePattern,
  publishInvalidation,
  createInvalidationSubscriber,
  getProductWithLock,
  INVALIDATION_CHANNEL,
} = require('./cache');

function makeDb() {
  const store = new Map([[1, { id: 1, name: 'Keyboard', price: 79 }]]);
  return {
    product: {
      findById: (id) => Promise.resolve(store.get(Number(id)) || null),
      update: (id, updates) => {
        const next = { ...(store.get(Number(id)) || { id: Number(id) }), ...updates, id: Number(id) };
        store.set(Number(id), next);
        return Promise.resolve(next);
      },
    },
  };
}

let redis, db;
beforeEach(() => {
  redis = new Redis();
  db = makeDb();
});

test('cacheProduct writes with TTL; updateProduct deletes then repopulates', async () => {
  await cacheProduct(redis, { id: 1, name: 'Keyboard', price: 79 });
  const ttl = await redis.ttl('product:1');
  assert.ok(ttl > 0 && ttl <= 300, `expected TTL in (0,300], got ${ttl}`);
  assert.deepStrictEqual(await getProduct(redis, 1), { id: 1, name: 'Keyboard', price: 79 });

  const updated = await updateProduct(redis, 1, { price: 69 }, db);
  assert.strictEqual(updated.price, 69);
  // Cache holds the fresh value, not the stale one.
  assert.strictEqual(JSON.parse(await redis.get('product:1')).price, 69);
});

test('invalidatePattern clears matching keys and counts real deletions', async () => {
  await redis.mset('product:1', 'a', 'product:2', 'b', 'product:3', 'c', 'order:1', 'x');
  const deleted = await invalidatePattern(redis, 'product:*');
  assert.strictEqual(deleted, 3);
  assert.strictEqual(await redis.get('product:1'), null);
  assert.strictEqual(await redis.get('order:1'), 'x'); // untouched
});

test('pub/sub invalidation drops the key from the L1 cache', async () => {
  const localCache = new Map([['product:1', { id: 1 }], ['product:2', { id: 2 }]]);
  const subscriber = createInvalidationSubscriber({}, Redis, localCache);
  await new Promise((resolve) => setTimeout(resolve, 50));

  await publishInvalidation(redis, ['product:1']);
  await new Promise((resolve) => setTimeout(resolve, 50));

  assert.strictEqual(localCache.has('product:1'), false);
  assert.strictEqual(localCache.has('product:2'), true);
  await subscriber.quit();
});

test('getProductWithLock populates the cache and clears the lock', async () => {
  const product = await getProductWithLock(redis, 1, db);
  assert.deepStrictEqual(product, { id: 1, name: 'Keyboard', price: 79 });
  assert.ok(JSON.parse(await redis.get('product:1')));
  assert.strictEqual(await redis.exists('lock:product:1'), 0);
});
