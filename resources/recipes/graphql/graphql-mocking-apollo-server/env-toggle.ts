// env-toggle.ts — Toggle mocking by environment
import { ApolloServer } from '@apollo/server';

// Option 1: Toggle mocks entirely
const server = new ApolloServer({
  typeDefs,
  resolvers: process.env.NODE_ENV === 'production' ? realResolvers : undefined,
  mocks: process.env.MOCK_API === 'true',
});

// Option 2: Combine real resolvers with mock fallback
const server2 = new ApolloServer({
  typeDefs,
  resolvers: realResolvers,
  mocks: process.env.NODE_ENV === 'development'
    ? { mocks, preserveResolvers: true }
    : false,
});
