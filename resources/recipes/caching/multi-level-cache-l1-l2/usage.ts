import { MultiLevelCache } from './multi-level-cache';

const cache = new MultiLevelCache('redis://localhost:6379', {
  l1MaxSize: 500,
  l1Ttl: 30_000,   // 30 seconds in L1
  l2Ttl: 300_000,  // 5 minutes in L2
});

await cache.connect();

// Get or load from database
const user = await cache.getOrLoad(
  `user:123`,
  () => db.users.findById(123),
  120_000, // 2 minutes TTL
);

// Invalidate after update
async function updateUser(id: string, data: Record<string, unknown>) {
  const user = await db.users.update(id, data);
  await cache.invalidate(`user:${id}`);
  return user;
}
