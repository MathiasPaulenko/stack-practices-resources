// Demo Express app for the StackPractices nodejs-redis-cache-invalidation
// recipe. Cache-aside reads, write-through updates, pub/sub invalidation of a
// local L1 Map, and a stampede lock — all against a real Redis on localhost.
const express = require('express');
const Redis = require('ioredis');
const {
  cacheProduct,
  getProduct,
  updateProduct,
  invalidatePattern,
  publishInvalidation,
  createInvalidationSubscriber,
  getProductWithLock,
} = require('./cache');

const redis = new Redis({ host: 'localhost', port: 6379 });
const localCache = new Map(); // L1 in-memory cache kept in sync via pub/sub
createInvalidationSubscriber({ host: 'localhost', port: 6379 }, Redis, localCache);

// In-memory stand-in for a database so the app runs with zero setup.
const products = new Map([
  [1, { id: 1, name: 'Keyboard', price: 79 }],
  [2, { id: 2, name: 'Mouse', price: 39 }],
  [3, { id: 3, name: 'Monitor', price: 249 }],
]);
const db = {
  product: {
    findById: async (id) => products.get(Number(id)) || null,
    update: async (id, updates) => {
      const current = products.get(Number(id)) || { id: Number(id) };
      const next = { ...current, ...updates, id: Number(id) };
      products.set(Number(id), next);
      return next;
    },
  },
};

const app = express();
app.use(express.json());

// Seed the demo data into Redis on startup.
app.locals.ready = (async () => {
  for (const product of products.values()) await cacheProduct(redis, product);
})();

// Cache-aside read with stampede lock. L1 first, then Redis, then DB.
app.get('/products/:id', async (req, res) => {
  const key = `product:${req.params.id}`;
  if (localCache.has(key)) return res.json({ source: 'l1', product: localCache.get(key) });

  const product = await getProductWithLock(redis, req.params.id, db);
  if (!product) return res.status(404).json({ error: 'not found' });

  localCache.set(key, product);
  res.json({ source: 'cache-aside', product });
});

// Write-through update: write DB, refresh Redis, broadcast invalidation so
// other instances drop the key from their L1 caches.
app.put('/products/:id', async (req, res) => {
  const product = await updateProduct(redis, req.params.id, req.body, db);
  await publishInvalidation(redis, [`product:${req.params.id}`]);
  res.json(product);
});

app.delete('/products/:id', async (req, res) => {
  products.delete(Number(req.params.id));
  await redis.del(`product:${req.params.id}`);
  localCache.delete(`product:${req.params.id}`);
  await publishInvalidation(redis, [`product:${req.params.id}`]);
  res.status(204).end();
});

// Pattern invalidation: clear every product key at once and tell the fleet.
app.post('/invalidate-products', async (req, res) => {
  const deleted = await invalidatePattern(redis, 'product:*');
  await publishInvalidation(redis, 'product:', 'pattern');
  res.json({ deleted });
});

// Inspect what the L1 cache currently holds (demo only).
app.get('/l1', (req, res) => {
  res.json(Object.fromEntries(localCache));
});

const PORT = process.env.PORT || 3000;
if (require.main === module) {
  app.locals.ready.then(() => {
    app.listen(PORT, () => console.log(`Listening on http://localhost:${PORT}`));
  });
}
module.exports = { app, db, redis, localCache };
