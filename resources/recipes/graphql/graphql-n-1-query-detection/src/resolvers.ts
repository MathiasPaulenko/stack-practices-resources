// BEFORE (N+1): uncomment this Post.author resolver and comment the
// batched one to watch the query log report 21 queries.
//
// Post: {
//   author: (post: { authorId: string }, _: unknown, ctx: any) =>
//     ctx.rawDb.users.findById(post.authorId),
// },

export const typeDefs = /* GraphQL */ `
  type User {
    id: ID!
    name: String!
  }

  type Post {
    id: ID!
    title: String!
    author: User
  }

  type Query {
    posts: [Post!]!
  }
`;

export const resolvers = {
  Query: {
    posts: (_: unknown, __: unknown, ctx: any) =>
      ctx.db.posts.findMany({ take: 20 }),
  },

  Post: {
    // DataLoader batches all authorIds into a single query.
    author: (post: { authorId: string }, _: unknown, ctx: any) =>
      ctx.loaders.user.load(post.authorId),
  },
};
