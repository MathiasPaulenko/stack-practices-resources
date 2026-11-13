// Fake database that counts queries and returns copies (like a real driver would).
export function createDb() {
  const users = new Map([
    ['u1', { id: 'u1', name: 'Ada' }],
    ['u2', { id: 'u2', name: 'Grace' }],
    ['u3', { id: 'u3', name: 'Linus' }],
  ]);

  const stats = { queries: 0 };

  return {
    stats,
    async findUsersByIds(ids) {
      stats.queries += 1;
      // Return copies so mutations can't silently rewrite cached objects.
      return ids.filter((id) => users.has(id)).map((id) => ({ ...users.get(id) }));
    },
    async updateUser(id, patch) {
      const u = users.get(id);
      if (u) users.set(id, { ...u, ...patch });
      return users.get(id) ? { ...users.get(id) } : null;
    },
  };
}
