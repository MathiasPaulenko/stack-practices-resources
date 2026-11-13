// The DataLoader contract, demonstrated: dedup per tick, positional order,
// per-key errors, prime/clear after mutation, loadMany, and cacheKeyFn.
// Run: npm install && node contract.mjs

import DataLoader from 'dataloader';
import { createDb } from './mock-db.mjs';

const db = createDb();

async function batchUsers(ids) {
  const rows = await db.findUsersByIds(ids);
  const map = new Map(rows.map((u) => [u.id, u]));
  // Order contract: index i must answer key ids[i].
  // Per-key errors: an Error at a position rejects only that caller.
  return ids.map((id) => map.get(id) ?? new Error(`User ${id} not found`));
}

// 1. Dedup + batching: 4 loads, 2 unique keys -> 1 query.
{
  const loader = new DataLoader(batchUsers);
  const [a, b, c, d] = await Promise.all([
    loader.load('u1'),
    loader.load('u1'),
    loader.load('u2'),
    loader.load('u1'),
  ]);
  console.log('dedup:', a.name, b.name, c.name, d.name, `(${db.stats.queries} query)`);
}

// 2. Per-key errors: u404 fails alone, u2 still resolves.
{
  const loader = new DataLoader(batchUsers);
  const results = await Promise.allSettled([loader.load('u2'), loader.load('u404')]);
  console.log(
    'per-key errors:',
    results[0].status,
    results[0].value.name,
    '|',
    results[1].status,
    results[1].reason.message,
  );
}

// 3. Mutation invalidation: clear() drops the stale entry.
{
  const loader = new DataLoader(batchUsers);
  const before = (await loader.load('u1')).name;
  await db.updateUser('u1', { name: 'Ada Lovelace' });
  const stale = (await loader.load('u1')).name; // still cached
  loader.clear('u1');
  const fresh = (await loader.load('u1')).name;
  console.log('cache invalidation:', { before, stale, fresh });
}

// 4. loadMany preserves input order, including not-found slots.
{
  const loader = new DataLoader(batchUsers);
  const results = await loader.loadMany(['u3', 'u404', 'u1']);
  console.log(
    'loadMany order:',
    results.map((r) => (r instanceof Error ? 'Error' : r.name)),
  );
}

// 5. cacheKeyFn makes object keys dedupe by value, not by reference.
{
  let calls = 0;
  const loader = new DataLoader(
    async (keys) => {
      calls += 1;
      const ids = keys.map((k) => k.id);
      const rows = await db.findUsersByIds(ids);
      const map = new Map(rows.map((u) => [u.id, u]));
      return keys.map((k) => map.get(k.id) ?? new Error('not found'));
    },
    { cacheKeyFn: (key) => key.id },
  );
  const [x, y] = await Promise.all([loader.load({ id: 'u1' }), loader.load({ id: 'u1' })]);
  console.log('cacheKeyFn: two object keys,', calls, 'batch call,', x.name === y.name);
}
