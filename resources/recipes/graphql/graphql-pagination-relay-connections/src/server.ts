// server.ts — minimal Apollo Server with an in-memory post store
import { ApolloServer } from '@apollo/server';
import { startStandaloneServer } from '@apollo/server/standalone';
import { typeDefs } from './schema';
import { postResolvers } from './resolvers';
import { encodeCursor } from './cursor';

// In-memory store shaped like a Prisma-ish client
const posts = Array.from({ length: 57 }, (_, i) => ({
  id: String(i + 1),
  title: `Post ${i + 1}`,
  content: `Content of post ${i + 1}`,
  createdAt: new Date(Date.now() - i * 3_600_000).toISOString(),
}));

const db = {
  posts: {
    findMany: async (opts: { take: number; skip: number; cursor?: { id: string }; orderBy: { id: 'asc' | 'desc' } }) => {
      let sorted = [...posts].sort((a, b) =>
        opts.orderBy.id === 'desc' ? Number(b.id) - Number(a.id) : Number(a.id) - Number(b.id)
      );
      if (opts.cursor) {
        sorted = sorted.filter((p) =>
          opts.orderBy.id === 'desc' ? Number(p.id) < Number(opts.cursor!.id) : Number(p.id) > Number(opts.cursor!.id)
        );
      }
      return sorted.slice(opts.skip, opts.skip + opts.take);
    },
    count: async () => posts.length,
  },
};

const server = new ApolloServer({ typeDefs, resolvers: postResolvers });

const { url } = await startStandaloneServer(server, {
  context: async () => ({ db }),
});

console.log(`GraphQL ready at ${url}`);
console.log('Try: query { posts(pagination: { first: 5 }) { edges { cursor node { id title } } pageInfo { hasNextPage endCursor } } }');
