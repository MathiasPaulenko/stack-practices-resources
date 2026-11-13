// demo.ts — proves N+1 vs batched behavior against the counting mock-db.
import { db, stats, resetStats, POSTS } from './mock-db.js';
import { createContext } from './context.js';

async function naiveAuthorLoads() {
  resetStats();
  const posts = await db.posts.findMany({ take: POSTS.length });
  for (const post of posts) {
    await db.users.findById(post.authorId); // one query per post -> N+1
  }
  return stats.queries;
}

async function batchedAuthorLoads() {
  resetStats();
  const ctx = createContext(db);
  const posts = await db.posts.findMany({ take: POSTS.length });
  await Promise.all(posts.map((p) => ctx.loaders.user.load(p.authorId)));
  return stats.queries;
}

async function main() {
  console.log('== N+1 vs DataLoader ==');
  const naive = await naiveAuthorLoads();
  console.log(`naive resolvers: ${naive} queries (1 list + ${POSTS.length} author lookups)`);
  const batched = await batchedAuthorLoads();
  console.log(`DataLoader:      ${batched} queries (1 list + 1 batched lookup)`);

  console.log('\n== Per-request cache dedupes repeated keys ==');
  resetStats();
  const ctx = createContext(db);
  await Promise.all([ctx.loaders.user.load('u1'), ctx.loaders.user.load('u1'), ctx.loaders.user.load('u1')]);
  console.log(`3x load("u1") -> ${stats.queries} query (deduped)`);

  console.log('\n== loadMany aligns results to keys ==');
  const many = await ctx.loaders.user.loadMany(['u3', 'u1']);
  console.log(`loadMany(['u3','u1']) -> ${many.map((v) => (v instanceof Error ? 'Error' : (v as { name: string }).name)).join(', ')}`);

  console.log('\n== Per-key errors do not sink the batch ==');
  const mixed = await ctx.loaders.user.loadMany(['u1', 'missing']);
  console.log(`loadMany(['u1','missing']) -> ${mixed.map((v) => (v instanceof Error ? v.message : (v as { name: string }).name)).join(' | ')}`);

  console.log('\n== Mutation invalidates the request cache ==');
  const before = await ctx.loaders.user.load('u1');
  await db.users.update({ where: { id: 'u1' }, data: { name: 'Ada Lovelace' } });
  ctx.loaders.user.clear('u1');
  const after = await ctx.loaders.user.load('u1');
  console.log(`name before: ${(before as { name: string }).name} -> after clear(): ${(after as { name: string }).name}`);

  console.log('\n== postsByAuthor (one-to-many) ==');
  const grouped = await ctx.loaders.postsByAuthor.loadMany(['u1', 'u3']);
  console.log(`u1 posts: ${(grouped[0] as { length: number }).length} | u3 posts: ${(grouped[1] as { length: number }).length} (1 batched query)`);
}

main();
