import { ApolloServer } from '@apollo/server';
import { buildSubgraphSchema } from '@apollo/subgraph';
import { startStandaloneServer } from '@apollo/server/standalone';

const orders = [
  { id: 'o1', userId: '1', total: 99.9 },
  { id: 'o2', userId: '1', total: 45.5 },
  { id: 'o3', userId: '2', total: 120.0 },
  { id: 'o4', userId: '3', total: 15.99 },
];

const typeDefs = `#graphql
  type Order @key(fields: "id") {
    id: ID!
    userId: ID!
    total: Float!
  }

  type User @key(fields: "id", resolvable: false) {
    id: ID! @external
    orders: [Order!]!
  }

  type Query {
    order(id: ID!): Order
  }
`;

const resolvers = {
  User: {
    orders(user: { id: string }) {
      return orders.filter((o) => o.userId === user.id);
    },
  },
  Query: {
    order(_: unknown, { id }: { id: string }) {
      return orders.find((o) => o.id === id);
    },
  },
};

const server = new ApolloServer({
  schema: buildSubgraphSchema([{ typeDefs, resolvers }]),
});

const { url } = await startStandaloneServer(server, {
  listen: { port: 4002 },
});
console.log(`Orders service ready at ${url}`);
