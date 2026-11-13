// SDL for the interface polymorphism pattern plus the seed data each
// resolver returns. Every data object carries __typename so __resolveType
// is a lookup, never a guess over which fields are non-null.
export const typeDefs = /* GraphQL */ `
  interface Node {
    id: ID!
    createdAt: String!
    updatedAt: String!
  }

  interface Searchable {
    id: ID!
    title: String!
    snippet: String!
    searchScore: Float!
  }

  type Post implements Node & Searchable {
    id: ID!
    createdAt: String!
    updatedAt: String!
    title: String!
    snippet: String!
    searchScore: Float!
    body: String!
    tags: [String!]!
    author: User!
  }

  type Comment implements Node {
    id: ID!
    createdAt: String!
    updatedAt: String!
    body: String!
    author: User!
    post: Post!
  }

  type User implements Node {
    id: ID!
    createdAt: String!
    updatedAt: String!
    name: String!
    email: String!
    posts: [Post!]!
  }

  type Query {
    feed: [Node!]!
    search(term: String!): [Searchable!]!
    node(id: ID!): Node
  }
`;

// Each row knows its concrete type; the resolver layer never inspects
// field shape to decide it.
export const db = {
  users: [
    {
      __typename: 'User',
      id: 'u1',
      createdAt: '2026-01-05T09:00:00Z',
      updatedAt: '2026-03-11T10:30:00Z',
      name: 'Ada',
      email: 'ada@example.com',
    },
  ],
  posts: [
    {
      __typename: 'Post',
      id: 'p1',
      createdAt: '2026-02-14T08:00:00Z',
      updatedAt: '2026-02-14T08:00:00Z',
      title: 'Interfaces in GraphQL',
      snippet: 'How interfaces share field contracts',
      searchScore: 9.4,
      body: 'Full post body',
      tags: ['graphql', 'schema'],
      authorId: 'u1',
    },
  ],
  comments: [
    {
      __typename: 'Comment',
      id: 'c1',
      createdAt: '2026-02-15T12:00:00Z',
      updatedAt: '2026-02-15T12:00:00Z',
      body: 'Nice write-up',
      authorId: 'u1',
      postId: 'p1',
    },
  ],
};
