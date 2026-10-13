import { ApolloServer } from '@apollo/server';
import { startStandaloneServer } from '@apollo/server/standalone';
import { typeDefs } from './schema.js';
import { resolvers } from './resolvers.js';
import { createContext } from './context.js';
import { authDirective } from './auth.js';

const server = new ApolloServer({
  schema: authDirective(typeDefs, resolvers),
  introspection: process.env.NODE_ENV !== 'production',
});

const { url } = await startStandaloneServer(server, {
  listen: { port: 4000 },
  context: async ({ req }) => createContext(req.headers.authorization),
});

console.log(`Server ready at ${url}`);
