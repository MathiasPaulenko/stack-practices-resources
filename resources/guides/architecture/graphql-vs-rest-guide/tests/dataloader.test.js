import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import { createHash } from 'node:crypto';
import { startRestServer, resetStats, stats } from '../rest-server.mjs';
import { startGraphql } from '../server.mjs';

const QUERY = `{ posts(limit: 10) { title author { name } } }`;
const PORT = 4055;

const runQuery = () =>
  fetch(`http://localhost:${PORT}/`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ query: QUERY }),
  }).then((r) => r.json());

let rest;
beforeAll(async () => { rest = await startRestServer(); });
afterAll(() => rest.close());

describe('N+1 vs DataLoader', () => {
  it('naive resolvers fan out into 1 + N REST requests', async () => {
    const gql = await startGraphql({ batched: false, port: PORT });
    try {
      resetStats();
      const res = await runQuery();
      expect(res.data.posts).toHaveLength(10);
      expect(stats.requests).toBe(11); // 1 posts list + 10 author fetches
    } finally {
      await gql.server.stop();
    }
  });

  it('DataLoader collapses author fetches into a single request', async () => {
    const gql = await startGraphql({ batched: true, port: PORT });
    try {
      resetStats();
      const res = await runQuery();
      expect(res.data.posts).toHaveLength(10);
      expect(stats.requests).toBe(2); // 1 posts list + 1 /users?ids=...
      expect(stats.paths[1]).toMatch(/^\/users\?ids=/);
      const post = res.data.posts[0];
      expect(Object.keys(post).sort()).toEqual(['author', 'title']);
      expect(Object.keys(post.author)).toEqual(['name']); // no id/email over-fetch
    } finally {
      await gql.server.stop();
    }
  });
});

describe('persisted queries', () => {
  it('query hashes are deterministic and shorter than the query text', () => {
    const longQuery = `{ posts(limit: 10) { id title createdAt author { id name email } comments { id body } } }`;
    const hash1 = createHash('sha256').update(longQuery).digest('hex');
    const hash2 = createHash('sha256').update(longQuery).digest('hex');
    expect(hash1).toBe(hash2);
    expect(`sha256:${hash1}`.length).toBeLessThan(longQuery.length);
  });
});
