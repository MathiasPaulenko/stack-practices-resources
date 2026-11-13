// posts-service.ts — subgraph owning Post and extending User.

import { ApolloServer } from '@apollo/server';
import { startStandaloneServer } from '@apollo/server/standalone';
import { buildSubgraphSchema } from '@apollo/subgraph';
import { gql } from 'graphql-tag';

const typeDefs = gql`
  type Post @key(fields: "id") {
    id: ID!
    title: String!
    content: String!
    author: User
  }

  type User @key(fields: "id") @extends {
    id: ID! @external
    posts: [Post!]!
  }

  type Query {
    posts: [Post!]!
    post(id: ID!): Post
  }
`;

const posts = [
  { id: '101', title: 'Hello', content: 'World', authorId: '1' },
  { id: '102', title: 'Federation', content: 'Guide', authorId: '2' },
];

const resolvers = {
  Query: {
    posts: () => posts,
    post: (_: unknown, { id }: { id: string }) => posts.find((p) => p.id === id),
  },
  Post: {
    author: (post: { authorId: string }) => ({ __typename: 'User', id: post.authorId }),
  },
  User: {
    posts: (user: { id: string }) => posts.filter((p) => p.authorId === user.id),
  },
};

export async function startPostsService(port = 4002) {
  const server = new ApolloServer({
    schema: buildSubgraphSchema([{ typeDefs, resolvers }]),
  });
  const { url } = await startStandaloneServer(server, { listen: { port } });
  console.log(`posts subgraph at ${url}`);
  return server;
}
