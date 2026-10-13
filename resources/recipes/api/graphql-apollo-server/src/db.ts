// In-memory stand-in for a real data source. Swap `db` for Prisma,
// a Postgres pool, or whatever your project uses — the resolver and
// loader shapes don't change.

export interface User {
  id: string;
  email: string;
  name: string;
}

export interface Post {
  id: string;
  title: string;
  content: string;
  authorId: string;
}

const users: User[] = [
  { id: 'u1', email: 'ada@example.com', name: 'Ada' },
  { id: 'u2', email: 'grace@example.com', name: 'Grace' },
];

const posts: Post[] = [
  { id: 'p1', title: 'Hello GraphQL', content: '...', authorId: 'u1' },
  { id: 'p2', title: 'N+1 explained', content: '...', authorId: 'u1' },
  { id: 'p3', title: 'Batching wins', content: '...', authorId: 'u2' },
];

export const db = {
  users: {
    findById: async (id: string) => users.find((u) => u.id === id),
    findMany: async (args?: { take?: number; where?: { id?: { in: string[] } } }) => {
      let result = users;
      if (args?.where?.id?.in) result = users.filter((u) => args.where!.id!.in.includes(u.id));
      return args?.take ? result.slice(0, args.take) : result;
    },
  },
  posts: {
    findMany: async (args?: { where?: { authorId?: string } }) =>
      args?.where?.authorId ? posts.filter((p) => p.authorId === args.where!.authorId) : posts,
    create: async (data: Omit<Post, 'id'>) => {
      const post: Post = { id: `p${posts.length + 1}`, ...data };
      posts.push(post);
      return post;
    },
  },
};

// Toy verifier: the token "demo" maps to the first user. Replace with
// your real verification (JWT signature, session store, introspection).
export const verifyToken = async (token: string): Promise<User | null> =>
  token === 'demo' ? users[0] : null;
