import { ApolloServer } from '@apollo/server';
import { startStandaloneServer } from '@apollo/server/standalone';
import { buildSchema } from './schema.mjs';
import { naiveResolvers, batchedResolvers } from './resolvers.mjs';

export async function startGraphql({ batched = true, port = 4000 } = {}) {
  const resolvers = batched ? batchedResolvers() : naiveResolvers;
  const server = new ApolloServer({ schema: buildSchema(resolvers) });
  const { url } = await startStandaloneServer(server, { listen: { port } });
  return { server, url };
}
