// The N+1 problem: one resolver call per post => one query per post.
// Run: node n-plus-one.mjs
// Requires nothing — plain Node.js.

import { createDb } from './mock-db.mjs';

const db = createDb();

const resolvers = {
  Post: {
    // Called once per post — 50 posts = 50 queries.
    author: (post) => db.findUserById(post.authorId),
  },
  Query: {
    posts: () => db.findPosts(),
  },
};

const posts = await resolvers.Query.posts();

const result = [];
for (const post of posts) {
  const author = await resolvers.Post.author(post);
  result.push({ ...post, author });
}

console.log(`Resolved ${result.length} posts with authors`);
console.log(`Total queries: ${db.queryCount}`); // 51 = 1 posts query + 50 author queries
