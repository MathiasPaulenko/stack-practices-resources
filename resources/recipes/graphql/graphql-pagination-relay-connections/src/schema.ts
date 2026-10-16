// schema.ts
import gql from 'graphql-tag';

export const typeDefs = gql`
  type PageInfo {
    hasNextPage: Boolean!
    hasPreviousPage: Boolean!
    startCursor: String
    endCursor: String
  }

  type PostEdge {
    cursor: String!
    node: Post!
  }

  type PostConnection {
    edges: [PostEdge!]!
    pageInfo: PageInfo!
    totalCount: Int!
  }

  type Post {
    id: ID!
    title: String!
    content: String!
    createdAt: String!
  }

  input PaginationInput {
    first: Int
    after: String
    last: Int
    before: String
  }

  type Query {
    posts(pagination: PaginationInput): PostConnection!
  }
`;
