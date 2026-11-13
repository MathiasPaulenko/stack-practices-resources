import { describe, expect, it } from 'vitest';
import {
  createPostSchema,
  eventSchema,
  updateUserSchema,
  validateInput,
} from '../src/schemas.ts';
import { ValidationException } from '../src/errors.ts';
import { resolvers } from '../src/resolvers.ts';

const ctx = {
  db: {
    posts: { create: async (d: Record<string, unknown>) => ({ id: 'p1', ...d }) },
    users: { update: async (id: string, d: Record<string, unknown>) => ({ id, ...d }) },
  },
  user: { id: 'u1' },
};

describe('validateInput', () => {
  it('returns typed data with transforms applied', () => {
    const r = validateInput(createPostSchema, {
      title: '  Padded title  ',
      content: 'This content is definitely long enough.',
      tags: [' graphql '],
    });
    expect(r.success).toBe(true);
    if (r.success) {
      expect(r.data.title).toBe('Padded title');
      expect(r.data.tags[0]).toBe('graphql');
    }
  });

  it('returns flat {field, message} errors', () => {
    const r = validateInput(createPostSchema, {
      title: 'Hi',
      content: 'short',
      tags: [],
      publishedAt: '2020-01-01T00:00:00Z',
    });
    expect(r.success).toBe(false);
    if (!r.success) {
      const fields = r.errors.map((e) => e.field);
      expect(fields).toContain('title');
      expect(fields).toContain('content');
      expect(fields).toContain('tags');
      expect(fields).toContain('publishedAt');
      expect(r.errors[0]).toHaveProperty('message');
    }
  });

  it('attaches cross-field errors to the chosen path', () => {
    const r = validateInput(eventSchema, {
      startDate: '2030-06-01T00:00:00Z',
      endDate: '2030-05-01T00:00:00Z',
    });
    expect(r.success).toBe(false);
    if (!r.success) expect(r.errors[0].field).toBe('endDate');
  });

  it('accepts empty-string website as an opt-out value', () => {
    const r = validateInput(updateUserSchema, { website: '' });
    expect(r.success).toBe(true);
  });
});

describe('resolvers', () => {
  it('throws ValidationException carrying field errors', async () => {
    await expect(
      resolvers.Mutation.createPost({}, { input: { title: 'x' } }, ctx)
    ).rejects.toBeInstanceOf(ValidationException);
    try {
      await resolvers.Mutation.createPost({}, { input: { title: 'x' } }, ctx);
    } catch (e) {
      const err = e as ValidationException;
      expect(err.validationErrors.length).toBeGreaterThan(0);
    }
  });

  it('persists validated data plus context fields', async () => {
    const post = await resolvers.Mutation.createPost(
      {},
      { input: { title: 'Good title', content: 'This content is long enough.', tags: ['t'] } },
      ctx
    ) as Record<string, unknown>;
    expect(post.authorId).toBe('u1');
    expect(post.title).toBe('Good title');
  });
});
