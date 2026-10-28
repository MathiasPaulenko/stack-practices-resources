/**
 * Cache stampede prevention — runnable simulation (Node stdlib only).
 *
 * Companion to https://stackpractices.com/patterns/cache-stampede-prevention-pattern/
 *
 * MiniRedis reproduces GET / SETEX / SET NX EX / check-and-delete with a Map
 * and real TTLs, so the coordination code matches the pattern in the article.
 * The demo fires 20 concurrent callers at a cold key and counts DB queries
 * per strategy: naive vs distributed lock vs stale-while-revalidate.
 *
 * Run: npx tsx src/stampede-demo.ts   (or transpile + node)
 */

type Entry = { value: string; expiresAt: number };

class MiniRedis {
  private data = new Map<string, Entry>();

  async get(key: string): Promise<string | null> {
    const e = this.data.get(key);
    if (!e) return null;
    if (e.expiresAt && Date.now() > e.expiresAt) {
      this.data.delete(key);
      return null;
    }
    return e.value;
  }

  async setex(key: string, ttlSec: number, value: string): Promise<void> {
    this.data.set(key, { value, expiresAt: Date.now() + ttlSec * 1000 });
  }

  async set(key: string, value: string, opts: { NX?: boolean; EX?: number } = {}): Promise<boolean> {
    const existing = this.data.get(key);
    if (opts.NX && existing && (!existing.expiresAt || Date.now() <= existing.expiresAt)) {
      return false;
    }
    this.data.set(key, { value, expiresAt: opts.EX ? Date.now() + opts.EX * 1000 : 0 });
    return true;
  }

  async deleteIfOwner(key: string, expected: string): Promise<number> {
    const e = this.data.get(key);
    if (e && e.value === expected) {
      this.data.delete(key);
      return 1;
    }
    return 0;
  }

  flush(): void {
    this.data.clear();
  }
}

class FakeDB {
  queries = 0;
  constructor(private latencyMs = 300) {}

  async query(key: string): Promise<unknown> {
    this.queries += 1;
    await new Promise((r) => setTimeout(r, this.latencyMs));
    return { key, payload: `row-for-${key}` };
  }
}

class NaiveCache {
  constructor(private store: MiniRedis, private db: FakeDB, private ttl = 60) {}

  async getOrLoad(key: string): Promise<unknown> {
    const cached = await this.store.get(key);
    if (cached !== null) return JSON.parse(cached);
    const value = await this.db.query(key);
    await this.store.setex(key, this.ttl, JSON.stringify(value));
    return value;
  }
}

class StampedeSafeCache {
  constructor(private store: MiniRedis, private db: FakeDB, private ttl = 60, private lockTimeout = 30) {}

  async getOrLoad(key: string): Promise<unknown> {
    const cached = await this.store.get(key);
    if (cached !== null) return JSON.parse(cached);

    const lockKey = `lock:${key}`;
    const lockValue = crypto.randomUUID();
    const acquired = await this.store.set(lockKey, lockValue, { NX: true, EX: this.lockTimeout });
    if (!acquired) return this.waitAndRead(key);

    try {
      const doubleCheck = await this.store.get(key); // double-check after winning
      if (doubleCheck !== null) return JSON.parse(doubleCheck);
      return await this.load(key);
    } finally {
      await this.store.deleteIfOwner(lockKey, lockValue);
    }
  }

  private async waitAndRead(key: string): Promise<unknown> {
    for (let i = 0; i < 20; i++) {
      await new Promise((r) => setTimeout(r, 50));
      const cached = await this.store.get(key);
      if (cached !== null) return JSON.parse(cached);
    }
    return this.load(key);
  }

  private async load(key: string): Promise<unknown> {
    const value = await this.db.query(key);
    await this.store.setex(key, this.ttl, JSON.stringify(value));
    return value;
  }
}

async function getSwr(
  store: MiniRedis,
  db: FakeDB,
  key: string,
  ttlMs = 500,
  staleWindowMs = 5000,
): Promise<unknown> {
  const packed = await store.get(key);
  if (packed !== null) {
    const entry = JSON.parse(packed) as { value: unknown; stored_at: number };
    const age = Date.now() - entry.stored_at;
    if (age < ttlMs) return entry.value;
    if (age < ttlMs + staleWindowMs) {
      // Past logical TTL, inside stale window — serve stale, refresh once.
      const claimed = await store.set(`refreshing:${key}`, "1", {
        NX: true,
        EX: Math.ceil(staleWindowMs / 1000),
      });
      if (claimed) void swrRefresh(store, db, key, ttlMs, staleWindowMs);
      return entry.value;
    }
  }
  return swrRefresh(store, db, key, ttlMs, staleWindowMs);
}

async function swrRefresh(
  store: MiniRedis,
  db: FakeDB,
  key: string,
  ttlMs: number,
  staleWindowMs: number,
): Promise<unknown> {
  const value = await db.query(key);
  const entry = { value, stored_at: Date.now() };
  await store.setex(key, Math.ceil((ttlMs + staleWindowMs) / 1000), JSON.stringify(entry));
  return value;
}

async function runStampede(
  name: string,
  worker: (key: string) => Promise<unknown>,
  callers: number,
  db: FakeDB,
): Promise<void> {
  await Promise.all(Array.from({ length: callers }, () => worker("hot-key")));
  console.log(`${name.padEnd(30)} callers=${callers}  db_queries=${db.queries}`);
}

async function main(): Promise<void> {
  const db = new FakeDB(300);
  const store = new MiniRedis();

  const naive = new NaiveCache(store, db);
  await runStampede("naive cache-aside", (k) => naive.getOrLoad(k), 20, db);

  db.queries = 0;
  store.flush();
  const safe = new StampedeSafeCache(store, db);
  await runStampede("distributed lock (SET NX EX)", (k) => safe.getOrLoad(k), 20, db);

  db.queries = 0;
  store.flush();
  // Seed an entry already past its logical TTL but inside the stale window.
  const seed = { value: await db.query("hot-key"), stored_at: Date.now() - 600 };
  await store.setex("hot-key", 60, JSON.stringify(seed));
  db.queries = 0;
  await runStampede(
    "stale-while-revalidate",
    (k) => getSwr(store, db, k, 500, 5000),
    20,
    db,
  );
  await new Promise((r) => setTimeout(r, 500)); // let the background refresh land
  console.log("\nExpected: naive ~20 queries; protected strategies ~1.");
}

void main();
