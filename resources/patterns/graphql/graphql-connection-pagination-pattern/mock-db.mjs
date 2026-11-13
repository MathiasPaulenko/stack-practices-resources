// In-memory "users" table shared by the demos.
// query() counts executions so the cost of each strategy is visible.

export function createDb() {
  const users = Array.from({ length: 95 }, (_, i) => ({
    id: `u${i + 1}`,
    name: `User ${i + 1}`,
    email: `user${i + 1}@example.com`,
    created_at: new Date(Date.UTC(2026, 0, 1) - i * 86_400_000).toISOString(),
  }));

  let queryCount = 0;

  return {
    users,
    get queryCount() {
      return queryCount;
    },

    // Simulates SELECT ... ORDER BY created_at DESC LIMIT n OFFSET m
    async queryOffset(limit, offset) {
      queryCount += 1;
      return users.slice(offset, offset + limit);
    },

    // Simulates SELECT ... WHERE (created_at, id) < ($1, $2) ORDER BY ... DESC LIMIT n
    async queryKeyset(createdAt, id, limit) {
      queryCount += 1;
      const start =
        createdAt == null
          ? 0
          : users.findIndex(
              (u) => u.created_at < createdAt || (u.created_at === createdAt && u.id < id)
            );
      return users.slice(Math.max(0, start), Math.max(0, start) + limit);
    },

    async count() {
      queryCount += 1;
      return users.length;
    },
  };
}
