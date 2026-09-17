/**
 * Write-behind cache with a durable dirty set in Redis (TypeScript).
 *
 * Mirrors write_behind_cache.py: dirty keys are tracked in a Redis set so
 * an application restart does not lose the flush queue. `db` is a
 * placeholder — wire it to your own client (pg, Prisma, Drizzle...).
 *
 * Requires: npm install redis (redis v4+).
 */

import { createClient } from 'redis';

const DIRTY_SET = 'writebehind:dirty';
const FLUSH_SET = 'writebehind:flushing';

type BatchItem = { key: string; value: unknown };
type DbWriter = (batch: BatchItem[]) => Promise<void>;

export class WriteBehindCache {
  private flushTimer: NodeJS.Timeout | null = null;

  constructor(
    private client: ReturnType<typeof createClient>,
    private dbWriter: DbWriter,
    private flushIntervalMs = 5000
  ) {
    this.flushTimer = setInterval(() => {
      this.flush().catch((err) => console.error('flush failed', err));
    }, this.flushIntervalMs);
  }

  async write<T>(key: string, value: T, ttl = 3600): Promise<T> {
    await this.client
      .multi()
      .set(key, JSON.stringify(value), { EX: ttl })
      .sAdd(DIRTY_SET, key)
      .exec();
    return value;
  }

  async flush(): Promise<void> {
    // RENAME is atomic: concurrent writes create a fresh DIRTY_SET.
    try {
      await this.client.rename(DIRTY_SET, FLUSH_SET);
    } catch {
      return; // no dirty keys
    }

    const keys = await this.client.sMembers(FLUSH_SET);
    const batch: BatchItem[] = [];
    for (const key of keys) {
      const raw = await this.client.get(key);
      if (raw !== null) batch.push({ key, value: JSON.parse(raw) });
    }

    try {
      if (batch.length > 0) await this.dbWriter(batch);
      await this.client.del(FLUSH_SET);
    } catch (error) {
      // Merge failed keys back into DIRTY_SET for the next cycle.
      await this.client.sUnionStore(DIRTY_SET, [DIRTY_SET, FLUSH_SET]);
      await this.client.del(FLUSH_SET);
      throw error;
    }
  }

  async dirtyCount(): Promise<number> {
    return this.client.sCard(DIRTY_SET);
  }

  async shutdown(): Promise<void> {
    if (this.flushTimer) clearInterval(this.flushTimer);
    await this.flush();
  }
}

// --- Usage example -------------------------------------------------------

declare const db: { query: (sql: string, values: unknown[]) => Promise<unknown> };

export async function demo(userId: string, name: string, email: string) {
  const redisClient = createClient({ url: 'redis://localhost:6379' });
  await redisClient.connect();

  const cache = new WriteBehindCache(
    redisClient,
    async (batch) => {
      const rows = batch.map((b) => b.value as { id: string; name: string; email: string });
      const values = rows.flatMap((r) => [r.id, r.name, r.email]);
      const placeholders = rows
        .map((_, i) => `($${i * 3 + 1}, $${i * 3 + 2}, $${i * 3 + 3})`)
        .join(', ');
      await db.query(
        `INSERT INTO users (id, name, email) VALUES ${placeholders}
         ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name, email = EXCLUDED.email`,
        values
      );
    },
    3000
  );

  await cache.write(`user:${userId}`, { id: userId, name, email });
  await cache.shutdown();
  await redisClient.quit();
}
