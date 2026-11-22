// lru-map.ts — Map-only LRU for small caches (a few hundred keys).
// delete + set re-appends a key; keys().next() is the least recently used.

export class MapLRUCache<K, V> {
  private cache = new Map<K, V>();

  constructor(private readonly capacity: number) {
    if (capacity <= 0) {
      throw new Error("Capacity must be positive");
    }
  }

  get(key: K): V | undefined {
    if (!this.cache.has(key)) return undefined;
    const value = this.cache.get(key)!;
    this.cache.delete(key);
    this.cache.set(key, value);
    return value;
  }

  set(key: K, value: V): void {
    if (this.cache.has(key)) {
      this.cache.delete(key);
    } else if (this.cache.size >= this.capacity) {
      const oldest = this.cache.keys().next().value;
      if (oldest !== undefined) this.cache.delete(oldest);
    }
    this.cache.set(key, value);
  }

  has(key: K): boolean {
    return this.cache.has(key);
  }

  get size(): number {
    return this.cache.size;
  }
}
