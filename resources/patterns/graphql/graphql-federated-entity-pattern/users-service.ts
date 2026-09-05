import { ApolloServer } from '@apollo/server';
import { buildSubgraphSchema } from '@apollo/subgraph';
import { startStandaloneServer } from '@apollo/server/standalone';

const users = [
  { id: '1', name: 'Ada Lovelace', email: 'ada@example.com' },
  { id: '2', name: 'Alan Turing', email: 'alan@example.com' },
  { id: '3', name: 'Grace Hopper', email: 'grace@example.com' },
];

const typeDefs = `#graphql
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

const resolvers = {
  User: {
    __resolveReference(user: { id: string }) {
      return users.find((u) => u.id === user.id);
    },
  },
  Query: {
    user(_: unknown, { id }: { id: string }) {
      return users.find((u) => u.id === id);
    },
    users() {
      return users;
    },
  },
};

const server = new ApolloServer({
  schema: buildSubgraphSchema([{ typeDefs, resolvers }]),
});

const { url } = await startStandaloneServer(server, {
  listen: { port: 4001 },
});
console.log(`Users service ready at ${url}`);
