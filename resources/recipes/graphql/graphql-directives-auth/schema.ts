// schema.ts — GraphQL type definitions with auth directives
import { gql } from 'graphql-tag';

export const typeDefs = gql`
  directive @auth(requires: Role = ADMIN) on FIELD_DEFINITION
  directive @owner on FIELD_DEFINITION
  directive @hasPermission(permission: String!) on FIELD_DEFINITION

  enum Role {
    ADMIN
    EDITOR
    VIEWER
  }

  type User {
    id: ID!
    name: String!
    email: String @auth(requires: ADMIN)
    role: Role @auth(requires: ADMIN)
    bio: String
  }

  type Post {
    id: ID!
    title: String!
    content: String!
    author: User!
    views: Int @auth(requires: EDITOR)
    draftContent: String @auth(requires: EDITOR) @owner
  }

  type Query {
    me: User @auth
    user(id: ID!): User @auth
    posts: [Post!]!
  }

  type Mutation {
    deletePost(id: ID!): Boolean @auth(requires: ADMIN)
  }
`;

// Minimal resolvers for testing
export const resolvers = {
  Query: {
    me: (_parent: any, _args: any, context: any) => {
      return context.user
        ? { id: context.user.id, name: 'Test User', email: 'test@example.com', role: context.user.role, bio: 'Bio' }
        : null;
    },
    user: (_parent: any, args: any, _context: any) => {
      return { id: args.id, name: 'User', email: 'user@example.com', role: 'VIEWER', bio: 'Bio', authorId: args.id };
    },
    posts: () => [
      { id: '1', title: 'Post 1', content: 'Content', authorId: '1', views: 100, draftContent: 'Draft' },
    ],
  },
  Post: {
    author: (parent: any) => ({ id: parent.authorId, name: 'Author', email: 'author@example.com', role: 'VIEWER', bio: 'Author bio' }),
  },
  Mutation: {
    deletePost: () => true,
  },
};
