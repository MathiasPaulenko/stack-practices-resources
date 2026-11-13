// The batched resolver with DataLoader: one query per batch window.
// Run: npm install && node batched-resolver.mjs

import DataLoader from 'dataloader';
import { createDb } from './mock-db.mjs';

const db = createDb();

async function batchLoadUsers(userIds) {
  // One query: SELECT * FROM users WHERE id IN (...)
  const users = await db.findUsersByIds(userIds);

  // DataLoader expects results in the same order as the input keys.
  const userMap = new Map(users.map((u) => [u.id, u]));
  return userIds.map(
    (id) => userMap.get(id) ?? new Error(`User ${id} not found`)
  );
}

// In a real server you create loaders inside the context factory,
// once per GraphQL request. Never share them across requests.
function createLoaders(context) {
  return {
    userLoader: new DataLoader((ids) => batchLoadUsers(ids, context), {
      cacheKeyFn: (key) => key.toString(),
    }),
  };
}

const loaders = createLoaders({ db });

const resolvers = {
  Post: {
    // All .load() calls in the same tick collapse into one batch.
    author: (post) => loaders.userLoader.load(post.authorId),
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
