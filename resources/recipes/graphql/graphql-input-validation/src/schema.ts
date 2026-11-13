export const typeDefs = /* GraphQL */ `
  input CreatePostInput {
    title: String!
    content: String!
    tags: [String!]!
    publishedAt: String
  }

  input UpdateUserInput {
    name: String
    bio: String
    website: String
  }

  type Post {
    id: ID!
    title: String!
    content: String!
    tags: [String!]!
    publishedAt: String
  }

  type User {
    id: ID!
    name: String
    bio: String
    website: String
  }

  type Mutation {
    createPost(input: CreatePostInput!): Post!
    updateUser(id: ID!, input: UpdateUserInput!): User!
  }

  type Query {
    _empty: String
  }
`;
