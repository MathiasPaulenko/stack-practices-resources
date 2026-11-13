import { createPostSchema, eventSchema, validateInput } from './schemas.ts';
import { ValidationException } from './errors.ts';
import { resolvers } from './resolvers.ts';

const db = {
  posts: { create: async (data: Record<string, unknown>) => ({ id: 'p1', ...data }) },
  users: { update: async (id: string, data: Record<string, unknown>) => ({ id, ...data }) },
};
const ctx = { db, user: { id: 'u1' } };

const badInput = {
  title: 'Hi',
  content: 'short',
  tags: [],
  publishedAt: '2020-01-01T00:00:00Z',
};

console.log('--- validateInput on invalid createPost ---');
const bad = validateInput(createPostSchema, badInput);
console.log(JSON.stringify(bad, null, 2));

console.log('\n--- validateInput on valid createPost (trims run) ---');
const good = validateInput(createPostSchema, {
  title: '  GraphQL validation in practice  ',
  content: 'Long enough content to pass the ten character minimum.',
  tags: [' graphql ', 'zod'],
  publishedAt: '2030-01-01T00:00:00Z',
});
console.log(JSON.stringify(good, null, 2));

console.log('\n--- cross-field refine on eventSchema ---');
console.log(JSON.stringify(
  validateInput(eventSchema, { startDate: '2030-06-01T00:00:00Z', endDate: '2030-05-01T00:00:00Z' }),
  null, 2
));

console.log('\n--- resolver: ValidationException thrown on bad input ---');
try {
  await resolvers.Mutation.createPost({}, { input: badInput }, ctx);
} catch (e) {
  if (e instanceof ValidationException) {
    console.log('ValidationException:', JSON.stringify(e.validationErrors));
  }
}

console.log('\n--- resolver: happy path returns created post ---');
const created = await resolvers.Mutation.createPost(
  {},
  { input: { title: 'Valid title here', content: 'Content that is long enough.', tags: ['a'] } },
  ctx
);
console.log(JSON.stringify(created));
