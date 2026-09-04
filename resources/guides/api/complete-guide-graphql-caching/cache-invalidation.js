// Event-driven cache invalidation with Redis pub/sub.
//
// After a mutation updates data, publish an invalidation event.
// Subscribers delete the cache entry and optionally purge CDN surrogate keys.

/**
 * Invalidate cache after a product update.
 * @param {object} redis - Redis client.
 * @param {number} productId - ID of the updated product.
 */
export async function invalidateProductCache(redis, productId) {
  await redis.del(`product:${productId}`);
  await redis.publish(
    "cache-invalidation",
    JSON.stringify({ type: "product", id: productId })
  );
}

/**
 * Subscribe to cache invalidation events.
 * @param {object} redis - Redis client.
 */
export function subscribeToInvalidation(redis) {
  redis.subscribe("cache-invalidation", (message) => {
    const { type, id } = JSON.parse(message);
    redis.del(`${type}:${id}`);
  });
}

/**
 * Versioned cache key helper.
 * Bump the version in Redis when data changes to invalidate all keys at once.
 * @param {object} redis - Redis client.
 * @param {string} entity - Entity type (e.g., "product").
 * @param {number} id - Entity ID.
 * @returns {Promise<string>} The versioned cache key.
 */
export async function versionedCacheKey(redis, entity, id) {
  const version = (await redis.get(`${entity}:version`)) || "1";
  return `${entity}:${id}:v${version}`;
}
