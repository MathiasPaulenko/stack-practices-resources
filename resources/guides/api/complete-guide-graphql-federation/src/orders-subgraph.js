const { buildSubgraphSchema } = require("@apollo/subgraph");
const { gql, ApolloServer } = require("apollo-server");

const typeDefs = gql`
  type Order @key(fields: "id") {
    id: ID!
    total: Float!
    status: String!
    userId: ID!
    user: User!
    items: [OrderItem!]!
  }

  type OrderItem {
    productId: ID!
    quantity: Int!
    price: Float!
  }

  extend type User @key(fields: "id") {
    id: ID! @external
    orders: [Order!]! @external
  }

  extend type Product @key(fields: "id") {
    id: ID! @external
    orders: [OrderItem!]!
  }

  type Query {
    order(id: ID!): Order
    orders: [Order!]!
  }

  type Mutation {
    createOrder(userId: ID!, items: [OrderItemInput!]!): Order!
  }

  input OrderItemInput {
    productId: ID!
    quantity: Int!
  }
`;

const resolvers = {
  Order: {
    user(order) {
      return { __typename: "User", id: order.userId };
    },
    items(order) {
      return order.items;
    },
  },
  Product: {
    orders(product) {
      return fetch(`http://orders-service/orders/items?productId=${product.id}`)
        .then((res) => res.json());
    },
  },
  Query: {
    order: (_, { id }) => fetch(`http://orders-service/orders/${id}`).then((res) => res.json()),
    orders: () => fetch("http://orders-service/orders").then((res) => res.json()),
  },
  Mutation: {
    createOrder: (_, { userId, items }) => {
      return fetch("http://orders-service/orders", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ userId, items }),
      }).then((res) => res.json());
    },
  },
};

const server = new ApolloServer({
  schema: buildSubgraphSchema([{ typeDefs, resolvers }]),
});

server.listen({ port: 4002 }).then(({ url }) => {
  console.log(`Orders subgraph ready at ${url}`);
});
