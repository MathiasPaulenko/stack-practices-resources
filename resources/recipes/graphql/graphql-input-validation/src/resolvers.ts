import { createPostSchema, updateUserSchema, validateInput } from './schemas.ts';
import { ValidationException } from './errors.ts';

interface Db {
  posts: { create: (data: Record<string, unknown>) => Promise<Record<string, unknown>> };
  users: { update: (id: string, data: Record<string, unknown>) => Promise<Record<string, unknown>> };
}

interface Context {
  db: Db;
  user: { id: string };
}

export const resolvers = {
  Mutation: {
    createPost: async (
      _: unknown,
      { input }: { input: unknown },
      ctx: Context
    ) => {
      const result = validateInput(createPostSchema, input);
      if (!result.success) {
        throw new ValidationException(result.errors);
      }

      return ctx.db.posts.create({
        ...result.data,
        authorId: ctx.user.id,
      });
    },

    updateUser: async (
      _: unknown,
      { id, input }: { id: string; input: unknown },
      ctx: Context
    ) => {
      const result = validateInput(updateUserSchema, input);
      if (!result.success) {
        throw new ValidationException(result.errors);
      }

      return ctx.db.users.update(id, result.data);
    },
  },
};
