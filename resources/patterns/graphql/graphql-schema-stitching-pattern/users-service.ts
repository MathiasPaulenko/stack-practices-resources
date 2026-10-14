// users-service.ts — Users subschema (users-api)
// Companion to https://stackpractices.com/patterns/graphql-schema-stitching-pattern/
import { makeExecutableSchema } from '@graphql-tools/schema';
import { ApolloServer } from '@apollo/server';
import { startStandaloneServer } from '@apollo/server/standalone';

export const usersTypeDefs = /* GraphQL */ `
  type User {
    id: ID!
    name: String!
    email: String!
  }

  type Query {
    user(id: ID!): User
    users: [User!]!
  }
`;

const users = [
  { id: '1', name: 'Ada Lovelace', email: 'ada@example.com' },
  { id: '2', name: 'Grace Hopper', email: 'grace@example.com' },
];

export const usersResolvers = {
  Query: {
    user: (_parent: unknown, args: { id: string }) =>
      users.find((u) => u.id === args.id) ?? null,
    users: () => users,
  },
};

// Run standalone: npx tsx users-service.ts  (serves :4001)
if (import.meta.url === `file://${process.argv[1]}`) {
  const server = new ApolloServer({
    schema: makeExecutableSchema({ typeDefs: usersTypeDefs, resolvers: usersResolvers }),
  });
  const { url } = await startStandaloneServer(server, { listen: { port: 4001 } });
  console.log(`users-api ready at ${url}`);
}
