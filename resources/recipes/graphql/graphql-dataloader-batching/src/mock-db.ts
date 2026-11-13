// mock-db.ts — in-memory tables that count every "database query" so the
// N+1 vs batched difference is measurable.
export type User = { id: string; name: string; email: string };
export type Post = { id: string; title: string; authorId: string };

export const USERS: User[] = [
  { id: 'u1', name: 'Ada', email: 'ada@example.com' },
  { id: 'u2', name: 'Grace', email: 'grace@example.com' },
  { id: 'u3', name: 'Linus', email: 'linus@example.com' },
];

export const POSTS: Post[] = [
  { id: 'p1', title: 'GraphQL basics', authorId: 'u1' },
  { id: 'p2', title: 'Resolvers deep dive', authorId: 'u1' },
  { id: 'p3', title: 'Schemas that scale', authorId: 'u2' },
  { id: 'p4', title: 'Federation notes', authorId: 'u3' },
  { id: 'p5', title: 'Error handling', authorId: 'u2' },
];

export const stats = { queries: 0 };

export function resetStats() {
  stats.queries = 0;
}

export const db = {
  users: {
    async findMany(opts: { where: { id: { in: string[] } } }): Promise<User[]> {
      stats.queries++;
      return USERS.filter((u) => opts.where.id.in.includes(u.id)).map((u) => ({ ...u }));
    },
    async findById(id: string): Promise<User | undefined> {
      stats.queries++;
      const u = USERS.find((u) => u.id === id);
      return u ? { ...u } : undefined;
    },
    async update(opts: { where: { id: string }; data: { name: string } }): Promise<User> {
      stats.queries++;
      const u = USERS.find((x) => x.id === opts.where.id);
      if (!u) throw new Error(`User ${opts.where.id} not found`);
      u.name = opts.data.name;
      return u;
    },
  },
  posts: {
    async findMany(opts?: { where?: { authorId?: { in: string[] } }; take?: number }): Promise<Post[]> {
      stats.queries++;
      let rows = POSTS;
      if (opts?.where?.authorId?.in) {
        rows = rows.filter((p) => opts.where!.authorId!.in.includes(p.authorId));
      }
      return rows.slice(0, opts?.take ?? rows.length);
    },
  },
};

export type Db = typeof db;
