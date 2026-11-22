import { LRUCache } from 'lru-cache';
import { createClient, RedisClientType } from 'redis';

export class MultiLevelCache {
  private l1: LRUCache<string, any>;
  private l2: RedisClientType;
  private pubsub: RedisClientType;
  private invalidationChannel: string;
  private l1TtlMs: number;
  private l2TtlMs: number;
  private ready: boolean = false;

  constructor(
    redisUrl: string = 'redis://localhost:6379',
    options: {
      l1MaxSize?: number;
      l1Ttl?: number;
      l2Ttl?: number;
      invalidationChannel?: string;
    } = {},
  ) {
    this.l1TtlMs = options.l1Ttl ?? 60_000;
    this.l2TtlMs = options.l2Ttl ?? 300_000;
    this.l1 = new LRUCache<string, any>({
      max: options.l1MaxSize ?? 1000,
      ttl: this.l1TtlMs,
      updateAgeOnGet: true,
    });

    this.l2 = createClient({ url: redisUrl });
    this.pubsub = createClient({ url: redisUrl });
    this.invalidationChannel = options.invalidationChannel ?? 'cache:invalidate';
  }

  async connect(): Promise<void> {
    await this.l2.connect();
    await this.pubsub.connect();
    await this.pubsub.subscribe(this.invalidationChannel, (message) => {
      const { key } = JSON.parse(message);
      this.l1.delete(key);
    });
    this.ready = true;
  }

  async disconnect(): Promise<void> {
    await this.pubsub.unsubscribe(this.invalidationChannel);
    await this.pubsub.quit();
    await this.l2.quit();
    this.l1.clear();
    this.ready = false;
  }

  async get<T>(key: string): Promise<T | undefined> {
    const l1Value = this.l1.get(key);
    if (l1Value !== undefined) {
      return l1Value as T;
    }

    const l2Value = await this.l2.get(key);
    if (l2Value !== null) {
      const parsed = JSON.parse(l2Value) as T;
      this.l1.set(key, parsed);
      return parsed;
    }

    return undefined;
  }

  async set<T>(key: string, value: T, ttl?: number): Promise<void> {
    const serialized = JSON.stringify(value);

    // Write to both levels; L2 always outlives L1
    this.l1.set(key, value, { ttl: ttl ?? this.l1TtlMs });
    await this.l2.set(key, serialized, {
      EX: Math.floor(Math.max(ttl ?? 0, this.l2TtlMs) / 1000),
    });
  }

  async getOrLoad<T>(
    key: string,
    loader: () => Promise<T>,
    ttl?: number,
  ): Promise<T> {
    const cached = await this.get<T>(key);
    if (cached !== undefined) {
      return cached;
    }

    const value = await loader();
    await this.set(key, value, ttl);
    return value;
  }

  async invalidate(key: string): Promise<void> {
    this.l1.delete(key);
    await this.l2.del(key);
    await this.l2.publish(
      this.invalidationChannel,
      JSON.stringify({ key }),
    );
  }

  async invalidatePattern(pattern: string): Promise<void> {
    for (const key of this.l1.keys()) {
      if (this._matchPattern(key, pattern)) {
        this.l1.delete(key);
      }
    }

    const keys = [];
    for await (const key of this.l2.scanIterator({ MATCH: pattern, COUNT: 100 })) {
      keys.push(key);
    }
    if (keys.length > 0) {
      await this.l2.del(keys);
    }

    await this.l2.publish(
      this.invalidationChannel,
      JSON.stringify({ pattern }),
    );
  }

  private _matchPattern(key: string, pattern: string): boolean {
    const regex = pattern.replace(/\*/g, '.*');
    return new RegExp(`^${regex}$`).test(key);
  }

  get stats() {
    return {
      l1Size: this.l1.size,
      l1MaxSize: this.l1.max,
      ready: this.ready,
    };
  }
}
