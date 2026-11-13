// users-service.ts — subgraph owning the User entity.

import { ApolloServer } from '@apollo/server';
import { startStandaloneServer } from '@apollo/server/standalone';
import { buildSubgraphSchema } from '@apollo/subgraph';
import { gql } from 'graphql-tag';

const typeDefs = gql`
  type User @key(fields: "id") {
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
  { id: '1', name: 'Alice', email: 'alice@example.com' },
  { id: '2', name: 'Bob', email: 'bob@example.com' },
];

const resolvers = {
  Query: {
    user: (_: unknown, { id }: { id: string }) => users.find((u) => u.id === id),
    users: () => users,
  },
  User: {
    __resolveReference: (ref: { id: string }) => users.find((u) => u.id === ref.id),
  },
};

export async function startUsersService(port = 4001) {
  const server = new ApolloServer({
    schema: buildSubgraphSchema([{ typeDefs, resolvers }]),
  });
  const { url } = await startStandaloneServer(server, { listen: { port } });
  console.log(`users subgraph at ${url}`);
  return server;
}
