import { ApolloServer } from '@apollo/server';
import { startStandaloneServer } from '@apollo/server/standalone';
import { ApolloGateway } from '@apollo/gateway';
import { AuthenticatedDataSource } from './authenticated-data-source.js';

const gateway = new ApolloGateway({
  serviceList: [
    { name: 'products', url: 'https://products-service.internal/graphql' },
    { name: 'reviews', url: 'https://reviews-service.internal/graphql' },
    { name: 'users', url: 'https://users-service.internal/graphql' },
    { name: 'orders', url: 'https://orders-service.internal/graphql' },
  ],
  // Poll for schema changes every 10 seconds in staging
  debug: process.env.NODE_ENV !== 'production',
  buildService({ url }) {
    return new AuthenticatedDataSource({ url });
  },
});

const server = new ApolloServer({
  gateway,
  // Subscriptions are not supported through the federation gateway
  subscriptions: false,
});

const { url } = await startStandaloneServer(server, {
  listen: { port: 4000 },
  context: async ({ req }) => ({
    user: authenticateUser(req),
    correlationId: req.headers['x-correlation-id'],
  }),
});

console.log(`gateway ready at ${url}`);
