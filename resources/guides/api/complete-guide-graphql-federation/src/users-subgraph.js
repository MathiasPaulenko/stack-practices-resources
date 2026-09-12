const { buildSubgraphSchema } = require("@apollo/subgraph");
const { gql, ApolloServer } = require("apollo-server");

const typeDefs = gql`
  type User @key(fields: "id") {
    id: ID!
    name: String!
    email: String!
    orders: [Order!]!
  }

  extend type Order @key(fields: "id") {
    id: ID! @external
    user: User! @provides(fields: "name")
  }

  extend type Product @key(fields: "id") {
    id: ID! @external
  }

  type Query {
    user(id: ID!): User
    users: [User!]!
  }
`;

const resolvers = {
  User: {
    orders(user) {
      return fetch(`http://orders-service/orders?userId=${user.id}`)
        .then((res) => res.json());
    },
  },
  Query: {
    user: (_, { id }) => fetch(`http://users-service/users/${id}`).then((res) => res.json()),
    users: () => fetch("http://users-service/users").then((res) => res.json()),
  },
};

const server = new ApolloServer({
  schema: buildSubgraphSchema([{ typeDefs, resolvers }]),
});

server.listen({ port: 4001 }).then(({ url }) => {
  console.log(`Users subgraph ready at ${url}`);
});
