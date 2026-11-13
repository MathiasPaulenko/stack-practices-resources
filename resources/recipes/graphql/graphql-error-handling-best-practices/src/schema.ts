// schema.ts — typeDefs + resolvers backed by an in-memory post store.

import {
  AuthenticationError,
  ConflictError,
  ForbiddenError,
  NotFoundError,
  ValidationError,
} from './errors.js';

export interface User {
  id: string;
  role: string;
}

export interface Post {
  id: string;
  slug: string;
  title: string;
  content: string;
  authorId: string;
}

export interface CreatePostInput {
  title: string;
  content: string;
  slug: string;
}

export interface Context {
  user: User | null;
}

const posts: Post[] = [
  { id: 'p1', slug: 'hello-world', title: 'Hello World', content: 'First post content', authorId: 'u1' },
  { id: 'p2', slug: 'graphql-tips', title: 'GraphQL Tips', content: 'Some longer content here', authorId: 'u2' },
];

export const typeDefs = /* GraphQL */ `
  type Post {
    id: ID!
    slug: String!
    title: String!
    content: String!
    authorId: ID!
  }

  input CreatePostInput {
    title: String!
    content: String!
    slug: String!
  }

  type Query {
    post(id: ID!): Post
    crash: String
  }

  type Mutation {
    createPost(input: CreatePostInput!): Post!
  }
`;

function validatePostInput(input: CreatePostInput): { field: string; message: string }[] {
  const errors: { field: string; message: string }[] = [];
  if (!input.title || input.title.length < 3) {
    errors.push({ field: 'title', message: 'Title must be at least 3 characters' });
  }
  if (!input.content || input.content.length < 10) {
    errors.push({ field: 'content', message: 'Content must be at least 10 characters' });
  }
  return errors;
}

export const resolvers = {
  Query: {
    post: async (_: unknown, { id }: { id: string }, ctx: Context) => {
      if (!ctx.user) throw new AuthenticationError();
      const post = posts.find((p) => p.id === id) ?? null;
      if (!post) throw new NotFoundError('Post', id);
      if (post.authorId !== ctx.user.id && ctx.user.role !== 'admin') {
        throw new ForbiddenError('You can only view your own posts', 'admin');
      }
      return post;
    },

    // Deliberately throws a non-GraphQL error to demo INTERNAL_ERROR masking.
    crash: async () => {
      throw new TypeError('Cannot read properties of undefined (reading "driver")');
    },
  },

  Mutation: {
    createPost: async (_: unknown, { input }: { input: CreatePostInput }, ctx: Context) => {
      if (!ctx.user) throw new AuthenticationError();

      const errors = validatePostInput(input);
      if (errors.length > 0) throw new ValidationError(errors);

      const existing = posts.find((p) => p.slug === input.slug);
      if (existing) throw new ConflictError('Slug already exists', { slug: input.slug });

      const post: Post = {
        id: `p${posts.length + 1}`,
        ...input,
        authorId: ctx.user.id,
      };
      posts.push(post);
      return post;
    },
  },
};
