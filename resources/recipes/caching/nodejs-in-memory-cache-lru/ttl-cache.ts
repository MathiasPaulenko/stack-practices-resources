// ttl-cache.ts — LRU with per-entry TTL and a periodic sweeper.
// cleanup() scans the whole Map: insertion order != expiry order when
// entries carry different TTLs, so an early break would skip expired keys.

interface CacheEntry<V> {
  value: V;
  expiresAt: number;
}

export class TTLCache<K, V> {
  private cache = new Map<K, CacheEntry<V>>();
  private cleanupTimer: NodeJS.Timeout | null = null;

  constructor(
    private readonly capacity: number,
    private readonly defaultTtl: number = 300_000,
  ) {}

  get(key: K): V | undefined {
    const entry = this.cache.get(key);
    if (!entry) return undefined;
    if (Date.now() > entry.expiresAt) {
      this.cache.delete(key);
      return undefined;
    }
    this.cache.delete(key);
    this.cache.set(key, entry);
    return entry.value;
  }

  set(key: K, value: V, ttl: number = this.defaultTtl): void {
    if (this.cache.has(key)) {
      this.cache.delete(key);
    } else if (this.cache.size >= this.capacity) {
      const oldest = this.cache.keys().next().value;
      if (oldest !== undefined) this.cache.delete(oldest);
    }
    this.cache.set(key, { value, expiresAt: Date.now() + ttl });
  }

  startCleanup(interval: number = 60_000): void {
    if (this.cleanupTimer) return;
    this.cleanupTimer = setInterval(() => this.cleanup(), interval);
    this.cleanupTimer.unref();
  }

  stopCleanup(): void {
    if (this.cleanupTimer) {
      clearInterval(this.cleanupTimer);
      this.cleanupTimer = null;
    }
  }

  private cleanup(): void {
    const now = Date.now();
    for (const [key, entry] of this.cache) {
      if (now > entry.expiresAt) {
        this.cache.delete(key);
      }
    }
  }

  get size(): number {
    return this.cache.size;
  }
}
