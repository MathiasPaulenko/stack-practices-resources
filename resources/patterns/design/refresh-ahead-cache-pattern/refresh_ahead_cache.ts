// Refresh-ahead cache pattern implementation in TypeScript.
// Requires: redis@^4.0, TypeScript 5+
// Usage: ts-node refresh_ahead_cache.ts

import { createClient, RedisClientType } from 'redis';

interface RefreshConfig {
  loader: () => Promise<unknown>;
  ttl: number;
}

class RefreshAheadCache {
  private redis: RedisClientType;
  private refreshCallbacks: Map<string, RefreshConfig> = new Map();
  private refreshThreshold: number;
  private refreshTimer: NodeJS.Timeout | null = null;
  private running: boolean = true;

  constructor(redisClient: RedisClientType, refreshThreshold = 0.8) {
    this.redis = redisClient;
    this.refreshThreshold = refreshThreshold;
    this.startRefreshLoop();
  }

  async register(key: string, loader: () => Promise<unknown>, ttl: number): Promise<void> {
    this.refreshCallbacks.set(key, { loader, ttl });
    await this.refreshKey(key);
  }

  async get<T>(key: string): Promise<T | null> {
    const cached = await this.redis.get(key);
    if (cached !== null) {
      return JSON.parse(cached) as T;
    }
    const config = this.refreshCallbacks.get(key);
    if (config) {
      return (await this.refreshKey(key)) as T;
    }
    return null;
  }

  private startRefreshLoop(): void {
    this.refreshTimer = setInterval(() => this.checkAndRefresh(), 10000);
  }

  private async checkAndRefresh(): Promise<void> {
    for (const [key, config] of this.refreshCallbacks) {
      const ttlRemaining = await this.redis.ttl(key);
      if (ttlRemaining < 0 || ttlRemaining < config.ttl * (1 - this.refreshThreshold)) {
        try {
          await this.refreshKey(key);
        } catch (error) {
          console.error(`Refresh failed for ${key}:`, error);
        }
      }
    }
  }

  private async refreshKey(key: string): Promise<unknown> {
    const config = this.refreshCallbacks.get(key)!;
    const value = await config.loader();
    await this.redis.set(key, JSON.stringify(value), { EX: config.ttl });
    return value;
  }

  async shutdown(): Promise<void> {
    this.running = false;
    if (this.refreshTimer) clearInterval(this.refreshTimer);
  }
}

// Example usage
async function main() {
  const redis = createClient({ url: 'redis://localhost:6379' });
  await redis.connect();

  const cache = new RefreshAheadCache(redis, 0.8);

  await cache.register(
    'product:featured',
    async () => [{ id: 1, name: 'Widget' }],
    300
  );

  const products = await cache.get<{ id: number; name: string }[]>('product:featured');
  console.log('Featured products:', products);

  await cache.shutdown();
  await redis.quit();
}

main().catch(console.error);
