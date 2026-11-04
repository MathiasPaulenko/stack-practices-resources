// Reference resolvers: payload errors + DataLoader batching.
// Expected failures go in the payload; unexpected ones propagate.
import DataLoader from "dataloader";

export const resolvers = {
  Mutation: {
    createUser: async (_root: unknown, { input }: { input: { email: string } }, ctx: any) => {
      const existing = await ctx.db.users.findUnique({ where: { email: input.email } });
      if (existing) {
        return {
          user: null,
          errors: [{ field: "email", message: "Email already in use", code: "CONFLICT" }],
        };
      }
      const user = await ctx.db.users.create({ data: input });
      return { user, errors: [] };
    },
  },
};

// Per-request loader (create inside the context factory, not globally):
// return value must align with the input array order or the batch misaligns.
export function createPostsLoader(db: any) {
  return new DataLoader(async (userIds: readonly number[]) => {
    const posts = await db.posts.findMany({ where: { authorId: { in: [...userIds] } } });
    const postsByAuthor = new Map<number, unknown[]>();
    for (const post of posts as any[]) {
      const list = postsByAuthor.get(post.authorId) ?? [];
      list.push(post);
      postsByAuthor.set(post.authorId, list);
    }
    return userIds.map((id) => postsByAuthor.get(id) ?? []);
  });
}
