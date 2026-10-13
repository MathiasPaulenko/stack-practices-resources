import { gql } from 'graphql-tag';

export const typeDefs = gql`
  directive @auth on FIELD_DEFINITION

  type User {
    id: ID!
    email: String!
    name: String!
    posts: [Post!]!
  }

  type Post {
    id: ID!
    title: String!
    content: String!
    author: User!
  }

  type Query {
    user(id: ID!): User
    users(limit: Int = 10): [User!]!
    posts: [Post!]!
  }

  type Mutation {
    createPost(title: String!, content: String!): Post! @auth
  }
`;
