/**
 * Cache-aside (lazy loading) with redis v4, TTL and stampede protection.
 *
 * The application checks the cache first; on a miss it loads from the
 * database, fills the cache with a TTL and returns the value. Writes go
 * to the database and then delete the cache key (invalidate, not update).
 *
 * The promise-dedup map is the single-flight: concurrent misses for the
 * same key share one database load instead of stampeding it.
 *
 * Requires: npm install redis, and a running Redis server.
 */

import type { RedisClientType } from "redis";

interface Db {
  query(sql: string, params: unknown[]): Promise<{ rows: Record<string, unknown>[] }>;
}

export class CacheAside<T> {
  private inflight = new Map<string, Promise<T | null>>();

  constructor(
    private redis: RedisClientType,
    private db: Db,
    private table: string,
    private ttlSec = 300,
  ) {}

  async get(id: string): Promise<T | null> {
    const key = `${this.table}:${id}`;

    // 1. Try cache
    const cached = await this.redis.get(key);
    if (cached !== null) return JSON.parse(cached) as T;

    // 2. Single-flight: one miss loads, the rest share the promise
    const pending = this.inflight.get(key);
    if (pending) return pending;

    const load = this.loadAndFill(key, id);
    this.inflight.set(key, load);
    try {
      return await load;
    } finally {
      this.inflight.delete(key);
    }
  }

  private async loadAndFill(key: string, id: string): Promise<T | null> {
    const res = await this.db.query(`SELECT * FROM ${this.table} WHERE id = $1`, [id]);
    if (res.rows.length === 0) return null;
    const value = res.rows[0] as T;
    await this.redis.setEx(key, this.ttlSec, JSON.stringify(value));
    return value;
  }

  /** Write path: update the database, then invalidate the cache key. */
  async update(id: string, data: Partial<T>, updateSql: string): Promise<void> {
    await this.db.query(updateSql, Object.values(data).concat(id));
    await this.redis.del(`${this.table}:${id}`);
  }
}
