import { readFileSync } from 'node:fs';
import { ApolloServer } from '@apollo/server';
import { startStandaloneServer } from '@apollo/server/standalone';
import { buildSubgraphSchema } from '@apollo/subgraph';
import { resolvers, createLoaders } from './resolvers.js';

const typeDefs = readFileSync(new URL('./products.graphqls', import.meta.url), 'utf8');

const server = new ApolloServer({
  schema: buildSubgraphSchema([{ typeDefs, resolvers }]),
});

const { url } = await startStandaloneServer(server, {
  listen: { port: 4001 },
  context: async ({ req }) => ({
    dataSources: createDataSources(req),
    loaders: createLoaders(db),
    user: authenticateUser(req),
  }),
});

console.log(`products subgraph ready at ${url}`);
