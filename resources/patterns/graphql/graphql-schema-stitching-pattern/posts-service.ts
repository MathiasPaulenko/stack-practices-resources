// posts-service.ts — Posts subschema (posts-api)
// Companion to https://stackpractices.com/patterns/graphql-schema-stitching-pattern/
import { makeExecutableSchema } from '@graphql-tools/schema';
import { ApolloServer } from '@apollo/server';
import { startStandaloneServer } from '@apollo/server/standalone';

export const postsTypeDefs = /* GraphQL */ `
  type Post {
    id: ID!
    title: String!
    body: String!
    authorId: ID!
  }

  type Query {
    post(id: ID!): Post
    posts: [Post!]!
    postsByAuthorIds(authorIds: [ID!]!): [Post!]!
  }
`;

const posts = [
  { id: '10', title: 'Analytical Engine notes', body: '…', authorId: '1' },
  { id: '11', title: 'Compilers and FLOW-MATIC', body: '…', authorId: '2' },
  { id: '12', title: 'Debugging the Mark II', body: '…', authorId: '2' },
];

export const postsResolvers = {
  Query: {
    post: (_parent: unknown, args: { id: string }) =>
      posts.find((p) => p.id === args.id) ?? null,
    posts: () => posts,
    postsByAuthorIds: (_parent: unknown, args: { authorIds: string[] }) =>
      posts.filter((p) => args.authorIds.includes(p.authorId)),
  },
};

// Run standalone: npx tsx posts-service.ts  (serves :4002)
if (import.meta.url === `file://${process.argv[1]}`) {
  const server = new ApolloServer({
    schema: makeExecutableSchema({ typeDefs: postsTypeDefs, resolvers: postsResolvers }),
  });
  const { url } = await startStandaloneServer(server, { listen: { port: 4002 } });
  console.log(`posts-api ready at ${url}`);
}
