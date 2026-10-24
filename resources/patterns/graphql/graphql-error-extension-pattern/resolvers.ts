import { ErrorCodes } from './error-codes';
import { GraphQLExtendedError } from './extended-error';

/**
 * Example resolvers throwing structured errors.
 * Assumes a context shaped as { db, user }.
 */
export const resolvers = {
  Query: {
    post: async (_parent: unknown, { id }: { id: string }, { db, user }: any) => {
      if (!user) {
        throw new GraphQLExtendedError(
          'Authentication required',
          ErrorCodes.UNAUTHENTICATED,
          { http: { status: 401 } }
        );
      }

      const post = await db.post.findById(id);
      if (!post) {
        throw new GraphQLExtendedError(
          `Post ${id} not found`,
          ErrorCodes.NOT_FOUND,
          { resourceId: id, http: { status: 404 } }
        );
      }

      if (post.authorId !== user.id && user.role !== 'admin') {
        throw new GraphQLExtendedError(
          "You don't have permission to view this post",
          ErrorCodes.FORBIDDEN,
          { http: { status: 403 } }
        );
      }

      return post;
    },
  },
  Mutation: {
    createPost: async (_parent: unknown, { input }: any, { db, user }: any) => {
      if (!user) {
        throw new GraphQLExtendedError(
          'Authentication required',
          ErrorCodes.UNAUTHENTICATED
        );
      }

      if (!input.title || input.title.trim().length === 0) {
        throw new GraphQLExtendedError(
          'Title is required',
          ErrorCodes.VALIDATION_ERROR,
          { field: 'title', constraint: 'required' }
        );
      }

      if (input.title.length > 200) {
        throw new GraphQLExtendedError(
          'Title must be 200 characters or less',
          ErrorCodes.VALIDATION_ERROR,
          { field: 'title', constraint: 'max_length', max: 200, actual: input.title.length }
        );
      }

      return db.post.create({ ...input, authorId: user.id });
    },
  },
};
