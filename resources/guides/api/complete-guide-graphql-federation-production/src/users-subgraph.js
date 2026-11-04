// Users subgraph: owns the User entity.
// __resolveReference is called once per entity representation —
// batch the lookups with a DataLoader (or an IN query) to avoid N+1.
const { buildSubgraphSchema } = require("@apollo/subgraph");
const { gql, ApolloServer } = require("@apollo/server");

const typeDefs = gql`
  type User @key(fields: "id") {
    id: ID!
    name: String!
    email: String!
  }

  type Query {
    user(id: ID!): User
  }
`;

const resolvers = {
  User: {
    __resolveReference: (reference, context) => {
      // Router sends { id: "123", __typename: "User" }
      return context.dataSources.users.getById(reference.id);
    },
  },
  Query: {
    user: (_root, { id }, context) => context.dataSources.users.getById(id),
  },
};

const server = new ApolloServer({
  schema: buildSubgraphSchema([{ typeDefs, resolvers }]),
});
