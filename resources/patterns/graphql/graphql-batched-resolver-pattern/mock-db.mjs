// Tiny in-memory "database" shared by the demos.
// Every method counts how many queries it would issue against a real backend.

export function createDb() {
  const users = new Map(
    Array.from({ length: 60 }, (_, i) => [
      `u${i + 1}`,
      { id: `u${i + 1}`, name: `User ${i + 1}` },
    ])
  );

  // 50 posts, several sharing the same author so deduplication is visible.
  const posts = Array.from({ length: 50 }, (_, i) => ({
    id: `p${i + 1}`,
    title: `Post ${i + 1}`,
    authorId: `u${(i % 30) + 1}`,
  }));

  let queryCount = 0;

  return {
    posts,
    get queryCount() {
      return queryCount;
    },
    reset() {
      queryCount = 0;
    },

    // Simulates: SELECT * FROM users WHERE id = $1
    async findUserById(id) {
      queryCount += 1;
      return users.get(id) ?? null;
    },

    // Simulates: SELECT * FROM users WHERE id IN (...)
    async findUsersByIds(ids) {
      queryCount += 1;
      return [...ids].map((id) => users.get(id)).filter(Boolean);
    },

    // Simulates: SELECT * FROM posts LIMIT 50
    async findPosts() {
      queryCount += 1;
      return posts;
    },
  };
}
