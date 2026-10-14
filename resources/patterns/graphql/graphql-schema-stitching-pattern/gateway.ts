// gateway.ts — Stitched gateway delegating to users-api and posts-api
// Companion to https://stackpractices.com/patterns/graphql-schema-stitching-pattern/
//
// Start users-service.ts (:4001) and posts-service.ts (:4002) first,
// then run: npx tsx gateway.ts  (serves :4000)
import { makeExecutableSchema } from '@graphql-tools/schema';
import { stitchSchemas } from '@graphql-tools/stitch';
import { buildHTTPExecutor } from '@graphql-tools/executor-http';
import { ApolloServer } from '@apollo/server';
import { startStandaloneServer } from '@apollo/server/standalone';
import { usersTypeDefs, usersResolvers } from './users-service.js';
import { postsTypeDefs, postsResolvers } from './posts-service.js';

// Executors send operations to the remote subschema endpoints over HTTP
const usersExecutor = buildHTTPExecutor({
  endpoint: 'http://localhost:4001/graphql',
});
const postsExecutor = buildHTTPExecutor({
  endpoint: 'http://localhost:4002/graphql',
});

const usersSubschema = {
  schema: makeExecutableSchema({ typeDefs: usersTypeDefs, resolvers: usersResolvers }),
  executor: usersExecutor,
};
const postsSubschema = {
  schema: makeExecutableSchema({ typeDefs: postsTypeDefs, resolvers: postsResolvers }),
  executor: postsExecutor,
};

// Link types create cross-service relationships at the gateway
const linkTypeDefs = /* GraphQL */ `
  extend type User {
    posts: [Post!]!
  }

  extend type Post {
    author: User!
  }
`;

const gatewaySchema = stitchSchemas({
  subschemas: [usersSubschema, postsSubschema],
  typeDefs: linkTypeDefs,
  resolvers: {
    User: {
      posts: {
        selectionSet: '{ id }',
        resolve: (user: { id: string }, _args: unknown, context: unknown, info: any) =>
          info.mergeInfo.delegateToSchema({
            schema: postsSubschema,
            operation: 'query',
            fieldName: 'posts',
            args: { authorId: user.id },
            context,
            info,
          }),
      },
    },
    Post: {
      author: {
        selectionSet: '{ authorId }',
        resolve: (post: { authorId: string }, _args: unknown, context: unknown, info: any) =>
          info.mergeInfo.delegateToSchema({
            schema: usersSubschema,
            operation: 'query',
            fieldName: 'user',
            args: { id: post.authorId },
            context,
            info,
          }),
      },
    },
  },
});

const server = new ApolloServer({ schema: gatewaySchema });
const { url } = await startStandaloneServer(server, { listen: { port: 4000 } });
console.log(`Gateway ready at ${url}`);
