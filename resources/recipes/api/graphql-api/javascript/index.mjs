// Apollo Server 4 standalone server from the recipe.
//
// Run:
//   npm install
//   node index.mjs
//
// Then open http://localhost:4000/ for Apollo Sandbox.

import { ApolloServer } from '@apollo/server';
import { startStandaloneServer } from '@apollo/server/standalone';

const typeDefs = `#graphql
  type Book {
    title: String!
    author: String!
    pages: Int!
  }

  type Query {
    books: [Book!]!
  }

  type Mutation {
    addBook(title: String!, author: String!, pages: Int!): Book!
  }
`;

const books = [
  { title: 'Clean Code', author: 'Robert C. Martin', pages: 464 },
  { title: 'The Pragmatic Programmer', author: 'Andy Hunt', pages: 352 },
];

const resolvers = {
  Query: {
    books: () => books,
  },
  Mutation: {
    addBook: (_, { title, author, pages }) => {
      const book = { title, author, pages };
      books.push(book);
      return book;
    },
  },
};

const server = new ApolloServer({ typeDefs, resolvers });
const { url } = await startStandaloneServer(server, {
  listen: { port: 4000 },
});
console.log(`Server ready at ${url}`);
