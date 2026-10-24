import { ApolloServer } from '@apollo/server';
import { startStandaloneServer } from '@apollo/server/standalone';
import { instrumentDbClient, type QueryLog } from './instrumented.js';
import { queryLoggerPlugin } from './queryLogger.js';
import { createUserLoader } from './loaders.js';
import { typeDefs, resolvers } from './resolvers.js';

// Minimal in-memory store so the example runs without a real database.
// Every method call goes through the proxy and is counted.
const users = Array.from({ length: 20 }, (_, i) => ({
  id: `u${i + 1}`,
  name: `User ${i + 1}`,
}));
const posts = Array.from({ length: 20 }, (_, i) => ({
  id: `p${i + 1}`,
  title: `Post ${i + 1}`,
  authorId: `u${(i % 20) + 1}`,
}));

const db = {
  posts: {
    async findMany({ take }: { take: number }) {
      return posts.slice(0, take);
    },
  },
  users: {
    async findMany({ where }: { where: { id: { in: string[] } } }) {
      return users.filter((u) => where.id.in.includes(u.id));
    },
    async findById(id: string) {
      return users.find((u) => u.id === id) ?? null;
    },
  },
};

interface Context {
  db: ReturnType<typeof instrumentDbClient>;
  rawDb: typeof db;
  queryLog: QueryLog;
  loaders: { user: ReturnType<typeof createUserLoader> };
}

const server = new ApolloServer<Context>({
  typeDefs,
  resolvers,
  plugins: [queryLoggerPlugin],
});

const { url } = await startStandaloneServer(server, {
  context: async () => {
    // Fresh counter + instrumented client + loaders per request.
    const queryLog: QueryLog = { count: 0, queries: [] };
    return {
      queryLog,
      db: instrumentDbClient(db, queryLog),
      rawDb: db,
      loaders: { user: createUserLoader(db) },
    };
  },
});

console.log(`Server ready at ${url}`);
console.log('Try: query { posts { id title author { name } } }');
