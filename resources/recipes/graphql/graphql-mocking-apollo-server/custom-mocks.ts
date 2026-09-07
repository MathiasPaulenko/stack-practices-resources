// custom-mocks.ts — Customize mocks with scalars using @faker-js/faker 8.x
import { ApolloServer } from '@apollo/server';
import { faker } from '@faker-js/faker';

const mocks = {
  ID: () => crypto.randomUUID(),
  String: () => 'Lorem ipsum',
  Int: () => Math.floor(Math.random() * 1000),
  Boolean: () => Math.random() > 0.5,
};

const server = new ApolloServer({
  typeDefs,
  mocks,
});
