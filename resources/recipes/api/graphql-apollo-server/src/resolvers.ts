import type { GraphQLContext } from './context.js';
import type { Post, User } from './db.js';

export const resolvers = {
  Query: {
    user: (_: unknown, { id }: { id: string }, ctx: GraphQLContext) =>
      ctx.db.users.findById(id),
    users: (_: unknown, { limit }: { limit: number }, ctx: GraphQLContext) =>
      ctx.db.users.findMany({ take: limit }),
    posts: (_: unknown, __: unknown, ctx: GraphQLContext) => ctx.db.posts.findMany(),
  },

  Mutation: {
    createPost: (
      _: unknown,
      args: { title: string; content: string },
      ctx: GraphQLContext,
    ) => ctx.db.posts.create({ ...args, authorId: ctx.user!.id }),
  },

  Post: {
    // Batched: N posts still produce one user query per request
    author: (post: Post, _: unknown, ctx: GraphQLContext) =>
      ctx.loaders.users.load(post.authorId),
  },

  User: {
    posts: (user: User, _: unknown, ctx: GraphQLContext) =>
      ctx.db.posts.findMany({ where: { authorId: user.id } }),
  },
};
