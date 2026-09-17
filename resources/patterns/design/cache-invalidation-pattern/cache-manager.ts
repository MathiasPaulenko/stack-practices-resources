/**
 * CacheManager — tag-based, versioned and write-through invalidation.
 * Companion to the Cache Invalidation Pattern resource on StackPractices.
 *
 * Requires a `redis` (node-redis v4+) client and a `db` object with an
 * `update(product)` method — wire it to your own data layer.
 */

import { createClient } from 'redis';

type RedisClient = ReturnType<typeof createClient>;

interface Product {
  id: string;
  categoryId: string;
  [key: string]: unknown;
}

declare const db: { update(product: Product): Promise<void> };

export class CacheManager {
  constructor(private redis: RedisClient) {}

  // Every cached key registers the tags it belongs to
  async setWithTags(key: string, value: unknown, tags: string[]): Promise<void> {
    await this.redis.setEx(key, 300, JSON.stringify(value));
    for (const tag of tags) {
      await this.redis.sAdd(`tag:${tag}`, key);
    }
  }

  // 1. Explicit invalidation: delete the key plus every tagged group.
  // Note: DEL does not glob — `del("products:category:*")` would only
  // remove a key literally named "products:category:*".
  async invalidateProduct(productId: string, categoryId: string): Promise<void> {
    await this.redis.del(`product:${productId}`);
    await this.invalidateByTag(`product:${productId}`);
    await this.invalidateByTag(`category:${categoryId}`);
  }

  // 2. Tag-based invalidation: delete every key registered under a tag
  async invalidateByTag(tag: string): Promise<void> {
    const keys = await this.redis.sMembers(`tag:${tag}`);
    if (keys.length > 0) await this.redis.del(keys);
    await this.redis.del(`tag:${tag}`);
  }

  // 3. Version-based invalidation: bump the namespace version
  async bumpVersion(namespace: string): Promise<void> {
    await this.redis.incr(`version:${namespace}`);
  }

  async getWithVersion<T>(namespace: string, key: string): Promise<T | null> {
    const version = (await this.redis.get(`version:${namespace}`)) ?? '1';
    const fullKey = `${namespace}:${version}:${key}`;
    const cached = await this.redis.get(fullKey);
    return cached ? (JSON.parse(cached) as T) : null;
  }

  // 4. Write-through: refresh the cache right after the DB write
  async updateProduct(product: Product): Promise<void> {
    await db.update(product);
    await this.setWithTags(`product:${product.id}`, product, [
      `product:${product.id}`,
      `category:${product.categoryId}`,
    ]);
  }
}

/**
 * Pub/sub invalidator — propagates invalidation events across instances.
 */
export class PubSubInvalidator {
  constructor(
    private publisher: RedisClient,
    private subscriber: RedisClient,
  ) {
    this.subscriber.subscribe('cache:invalidate', (message) => {
      const data = JSON.parse(message);
      if (data.key) {
        this.publisher.del(data.key);
      } else if (data.pattern) {
        this.publisher.keys(data.pattern).then((keys) => {
          if (keys.length > 0) this.publisher.del(keys);
        });
      }
    });
  }

  async invalidate(key: string): Promise<void> {
    await this.publisher.del(key);
    await this.publisher.publish('cache:invalidate', JSON.stringify({ key }));
  }

  async invalidatePattern(pattern: string): Promise<void> {
    const keys = await this.publisher.keys(pattern);
    if (keys.length > 0) await this.publisher.del(keys);
    await this.publisher.publish(
      'cache:invalidate',
      JSON.stringify({ pattern }),
    );
  }
}
