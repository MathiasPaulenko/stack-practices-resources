// demo.ts — drives the Apollo Server in-process and prints real error responses.
// Run: npm start

import { HeaderMap } from '@apollo/server';
import { createServer } from './server.js';
import type { Context, User } from './schema.js';

const viewer: User = { id: 'u1', role: 'user' };
const admin: User = { id: 'u9', role: 'admin' };

const GET_POST = /* GraphQL */ `
  query GetPost($id: ID!) {
    post(id: $id) { id title authorId }
  }
`;

const CREATE_POST = /* GraphQL */ `
  mutation CreatePost($input: CreatePostInput!) {
    createPost(input: $input) { id slug title }
  }
`;

const CRASH = /* GraphQL */ `query { crash }`;

interface Case {
  label: string;
  query: string;
  variables?: Record<string, unknown>;
  user: User | null;
}

const cases: Case[] = [
  { label: 'UNAUTHENTICATED (no user in context)', query: GET_POST, variables: { id: 'p1' }, user: null },
  { label: 'FORBIDDEN (u2 asks for u1 post as viewer)', query: GET_POST, variables: { id: 'p2' }, user: viewer },
  { label: 'NOT_FOUND (valid user, missing post)', query: GET_POST, variables: { id: 'p404' }, user: viewer },
  {
    label: 'VALIDATION_ERROR (title too short)',
    query: CREATE_POST,
    variables: { input: { title: 'Hi', content: 'short', slug: 'x' } },
    user: viewer,
  },
  {
    label: 'CONFLICT (slug already exists)',
    query: CREATE_POST,
    variables: { input: { title: 'Dup', content: 'long enough content', slug: 'hello-world' } },
    user: viewer,
  },
  {
    label: 'Happy path (admin reads any post)',
    query: GET_POST,
    variables: { id: 'p2' },
    user: admin,
  },
  { label: 'INTERNAL_SERVER_ERROR masking (unexpected throw)', query: CRASH, user: viewer },
];

async function run() {
  const server = createServer();
  await server.start();

  for (const c of cases) {
    const response = await server.executeHTTPGraphQLRequest({
      httpGraphQLRequest: {
        method: 'POST',
        headers: new HeaderMap([['content-type', 'application/json']]),
        search: '',
        body: { query: c.query, variables: c.variables ?? {} },
      },
      context: async (): Promise<Context> => ({ user: c.user }),
    });

    const body = response.body.kind === 'complete' ? JSON.parse(response.body.string) : response.body;
    const codes = (body.errors ?? []).map(
      (e: { extensions?: { code?: string } }) => e.extensions?.code ?? '(no code)',
    );

    console.log(`\n=== ${c.label}`);
    console.log(`status: ${response.status ?? 200} | codes: ${codes.length ? codes.join(', ') : '(none)'}`);
    console.log(JSON.stringify(body, null, 2));
  }

  await server.stop();
}

run().catch((err) => {
  console.error(err);
  process.exit(1);
});
