// server.ts — Apollo Server setup with directive transformers
import { ApolloServer } from '@apollo/server';
import { startStandaloneServer } from '@apollo/server/standalone';
import { makeExecutableSchema } from '@graphql-tools/schema';
import { authDirectiveTransformer } from './directives/auth';
import { ownerDirectiveTransformer } from './directives/owner';
import { typeDefs, resolvers } from './schema';

let schema = makeExecutableSchema({ typeDefs, resolvers });
schema = authDirectiveTransformer(schema);
schema = ownerDirectiveTransformer(schema);

const server = new ApolloServer({ schema });

startStandaloneServer(server, {
  context: async ({ req }) => ({
    user: req.headers.authorization ? { id: '1', role: 'EDITOR' } : null,
  }),
}).then(({ url }) => console.log(`Server ready at ${url}`));
