// resolvers.ts
import { encodeCursor, decodeCursor } from './cursor';

interface Post {
  id: string;
  title: string;
  content: string;
  createdAt: string;
}

export const postResolvers = {
  Query: {
    posts: async (
      _: unknown,
      { pagination }: { pagination: { first?: number; after?: string; last?: number; before?: string } },
      context: { db: { posts: { findMany: (opts: any) => Promise<Post[]>; count: () => Promise<number> } } }
    ) => {
      const { first, after, last, before } = pagination;
      const limit = first ?? last ?? 10;
      const maxLimit = 50;

      const take = Math.min(limit, maxLimit);

      let cursor: string | undefined;
      let skip = 0;
      let order: 'asc' | 'desc' = 'desc';

      if (after) {
        cursor = decodeCursor(after);
        skip = 1;
      } else if (before) {
        cursor = decodeCursor(before);
        skip = 1;
        order = 'asc';
      }

      const posts = await context.db.posts.findMany({
        take: take + 1,
        skip,
        cursor: cursor ? { id: cursor } : undefined,
        orderBy: { id: order },
      });

      const hasMore = posts.length > take;
      const trimmed = hasMore ? posts.slice(0, take) : posts;
      const reversed = last ? trimmed.reverse() : trimmed;

      const edges = reversed.map((post) => ({
        cursor: encodeCursor(post.id),
        node: post,
      }));

      const totalCount = await context.db.posts.count();

      // hasMore means "more rows exist in the direction you queried":
      // forward (first/after) → hasNextPage; backward (last/before) → hasPreviousPage
      return {
        edges,
        totalCount,
        pageInfo: {
          hasNextPage: before ? true : Boolean(first && hasMore),
          hasPreviousPage: after ? true : Boolean(last && hasMore),
          startCursor: edges[0]?.cursor ?? null,
          endCursor: edges[edges.length - 1]?.cursor ?? null,
        },
      };
    },
  },
};
