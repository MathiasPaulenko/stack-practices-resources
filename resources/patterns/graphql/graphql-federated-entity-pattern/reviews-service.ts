import { ApolloServer } from '@apollo/server';
import { buildSubgraphSchema } from '@apollo/subgraph';
import { startStandaloneServer } from '@apollo/server/standalone';

const reviews = [
  { id: 'r1', userId: '1', productId: 'p1', rating: 5, comment: 'Excellent' },
  { id: 'r2', userId: '1', productId: 'p2', rating: 3, comment: 'OK' },
  { id: 'r3', userId: '2', productId: 'p1', rating: 4, comment: 'Good' },
];

const typeDefs = `#graphql
  type Review @key(fields: "id") {
    id: ID!
    userId: ID!
    productId: ID!
    rating: Int!
    comment: String
  }

  type User @key(fields: "id", resolvable: false) {
    id: ID! @external
    reviews: [Review!]!
  }

  type Query {
    review(id: ID!): Review
  }
`;

const resolvers = {
  User: {
    reviews(user: { id: string }) {
      return reviews.filter((r) => r.userId === user.id);
    },
  },
  Query: {
    review(_: unknown, { id }: { id: string }) {
      return reviews.find((r) => r.id === id);
    },
  },
};

const server = new ApolloServer({
  schema: buildSubgraphSchema([{ typeDefs, resolvers }]),
});

const { url } = await startStandaloneServer(server, {
  listen: { port: 4003 },
});
console.log(`Reviews service ready at ${url}`);
