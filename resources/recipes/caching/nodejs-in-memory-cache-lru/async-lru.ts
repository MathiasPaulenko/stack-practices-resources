// async-lru.ts — async LRU that stores promises and never caches rejections.

export class AsyncLRUCache<K, V> {
  private cache = new Map<K, { promise: Promise<V>; expiresAt: number }>();

  constructor(
    private readonly capacity: number,
    private readonly ttl: number = 300_000,
  ) {}

  async get(key: K, loader: () => Promise<V>): Promise<V> {
    const entry = this.cache.get(key);
    if (entry && Date.now() < entry.expiresAt) {
      this.cache.delete(key);
      this.cache.set(key, entry);
      return entry.promise;
    }

    const promise = loader().then(
      (v) => v,
      (err) => {
        this.cache.delete(key); // failed loads leave no poisoned entry
        throw err;
      },
    );
    this.cache.set(key, { promise, expiresAt: Date.now() + this.ttl });

    if (this.cache.size > this.capacity) {
      const oldest = this.cache.keys().next().value;
      if (oldest !== undefined) this.cache.delete(oldest);
    }

    return promise;
  }

  get size(): number {
    return this.cache.size;
  }
}
