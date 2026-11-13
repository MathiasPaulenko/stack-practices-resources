import { makeExecutableSchema } from '@graphql-tools/schema';
import gql from 'graphql-tag';

const typeDefs = gql`
  type User { id: ID! name: String! email: String! }
  type Comment { id: ID! body: String! }
  type Post {
    id: ID!
    title: String!
    createdAt: String!
    author: User
    comments: [Comment!]!
  }
  type Query { posts(limit: Int): [Post!]! post(id: ID!): Post }
`;

export const buildSchema = (resolvers) =>
  makeExecutableSchema({ typeDefs, resolvers });
