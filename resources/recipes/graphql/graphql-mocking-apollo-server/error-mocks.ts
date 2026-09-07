// error-mocks.ts — Simulate error responses for UI testing
import { ApolloServer } from '@apollo/server';

const mocks = {
  Query: () => ({
    user: () => { throw new Error('User not found'); },
  }),
};

const server = new ApolloServer({
  typeDefs,
  mocks,
});
