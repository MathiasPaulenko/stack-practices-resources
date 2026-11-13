// The same pattern without any library: collect keys, query once, distribute.
// Run: node manual-batch.mjs — no dependencies.

import { createDb } from './mock-db.mjs';

const db = createDb();

// A minimal manual batcher: one microtask window, Set for dedup,
// positional mapping back to callers.
function createBatcher(batchFn) {
  let queue = [];
  let scheduled = false;

  return {
    load(key) {
      return new Promise((resolve) => {
        queue.push({ key, resolve });
        if (!scheduled) {
          scheduled = true;
          queueMicrotask(async () => {
            const batch = queue;
            queue = [];
            scheduled = false;
            const uniqueKeys = [...new Set(batch.map((entry) => entry.key))];
            const results = await batchFn(uniqueKeys);
            const byKey = new Map(uniqueKeys.map((key, i) => [key, results[i]]));
            for (const entry of batch) entry.resolve(byKey.get(entry.key));
          });
        }
      });
    },
  };
}

const userBatcher = createBatcher(async (ids) => {
  const users = await db.findUsersByIds(ids); // one query for the whole window
  return ids.map((id) => users.find((u) => u.id === id) ?? null);
});

const resolvers = {
  Post: {
    author: (post) => userBatcher.load(post.authorId),
  },
  Query: {
    posts: () => db.findPosts(),
  },
};

const posts = await resolvers.Query.posts();

const result = await Promise.all(
  posts.map(async (post) => ({
    ...post,
    author: await resolvers.Post.author(post),
  }))
);

console.log(`Resolved ${result.length} posts with authors`);
console.log(`Total queries: ${db.queryCount}`); // 2 = 1 posts query + 1 batched users query
