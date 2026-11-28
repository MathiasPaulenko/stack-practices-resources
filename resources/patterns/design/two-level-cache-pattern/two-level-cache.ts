import { createClient } from 'redis';

type RedisClient = ReturnType<typeof createClient>;

export class TwoLevelCache {
  private l1: Map<string, { value: any; expiry: number }> = new Map();
  private l1MaxSize: number;
  private l1TtlMs: number;
  private l2Ttl: number;
  private redis: RedisClient;

  constructor(redisClient: RedisClient, l1MaxSize = 1000, l1TtlMs = 60000, l2Ttl = 3600) {
    this.redis = redisClient;
    this.l1MaxSize = l1MaxSize;
    this.l1TtlMs = l1TtlMs;
    this.l2Ttl = l2Ttl;
  }

  async get<T>(key: string, loader: () => Promise<T>): Promise<T> {
    const l1Entry = this.l1.get(key);
    if (l1Entry && Date.now() < l1Entry.expiry) {
      this.l1.delete(key);
      this.l1.set(key, l1Entry);
      return l1Entry.value as T;
    }
    this.l1.delete(key);

    const l2Cached = await this.redis.get(key);
    if (l2Cached !== null) {
      const value = JSON.parse(l2Cached) as T;
      this.populateL1(key, value);
      return value;
    }

    const value = await loader();
    this.populateL1(key, value);
    await this.redis.set(key, JSON.stringify(value), { EX: this.l2Ttl });
    return value;
  }

  private populateL1(key: string, value: any): void {
    if (this.l1.size >= this.l1MaxSize) {
      const oldestKey = this.l1.keys().next().value;
      if (oldestKey) this.l1.delete(oldestKey);
    }
    this.l1.set(key, { value, expiry: Date.now() + this.l1TtlMs });
  }

  invalidate(key: string): void {
    this.l1.delete(key);
    this.redis.del(key);
    this.redis.publish('cache:invalidate', key);
  }
}
