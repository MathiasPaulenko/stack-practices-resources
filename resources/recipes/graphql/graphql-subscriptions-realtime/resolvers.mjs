import { PubSub, withFilter } from 'graphql-subscriptions';

export const pubsub = new PubSub();
export const POST_CREATED = 'POST_CREATED';
export const POST_UPDATED = 'POST_UPDATED';

const rows = [
  { id: '1', title: 'Hello', content: 'First post', authorId: 'u1', createdAt: '2026-01-01T00:00:00Z' },
  { id: '2', title: 'Second', content: 'Another one', authorId: 'u2', createdAt: '2026-01-02T00:00:00Z' },
];

export const db = {
  posts: {
    findMany() { return rows; },
    create(post) {
      const created = { id: String(rows.length + 1), ...post };
      rows.push(created);
      return created;
    },
    update(id, patch) {
      const post = rows.find((p) => p.id === id);
      if (!post) throw new Error(`Post ${id} not found`);
      Object.assign(post, Object.fromEntries(Object.entries(patch).filter(([, v]) => v != null)));
      return post;
    },
  },
};

export const resolvers = {
  Query: {
    posts: (_p, _a, ctx) => ctx.db.posts.findMany(),
  },

  Mutation: {
    createPost: (_p, args, ctx) => {
      const post = ctx.db.posts.create({
        title: args.title,
        content: args.content,
        authorId: ctx.user.id,
        createdAt: new Date().toISOString(),
      });
      // Payload key must match the subscription field name
      pubsub.publish(POST_CREATED, { postCreated: post });
      return post;
    },

    updatePost: (_p, args, ctx) => {
      const post = ctx.db.posts.update(args.id, {
        title: args.title,
        content: args.content,
        updatedBy: ctx.user.id,
      });
      pubsub.publish(POST_UPDATED, { postUpdated: post });
      return post;
    },
  },

  Subscription: {
    postCreated: {
      subscribe: () => pubsub.asyncIterator([POST_CREATED]),
    },
    postUpdated: {
      subscribe: withFilter(
        () => pubsub.asyncIterator([POST_UPDATED]),
        (payload, { id }) => payload.postUpdated.id === id,
      ),
    },
  },
};
