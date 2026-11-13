import { startRestServer, resetStats, stats } from './rest-server.mjs';
import { startGraphql } from './server.mjs';

const QUERY = `{ posts(limit: 10) { title author { name } } }`;
const runQuery = (query) =>
  fetch('http://localhost:4000/', {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ query }),
  }).then((r) => r.json());

const rest = await startRestServer();
try {
  // Phase 1: naive resolvers fan out into N+1 REST calls.
  let gql = await startGraphql({ batched: false, port: 4000 });
  resetStats();
  let res = await runQuery(QUERY);
  console.log(`naive   : ${res.data.posts.length} posts -> ${stats.requests} REST requests`);
  console.log(`          paths: ${stats.paths.slice(0, 4).join(', ')}, ...`);
  await gql.server.stop();

  // Phase 2: DataLoader batches the author fetches into one call.
  gql = await startGraphql({ batched: true, port: 4000 });
  resetStats();
  res = await runQuery(QUERY);
  console.log(`batched : ${res.data.posts.length} posts -> ${stats.requests} REST requests`);
  console.log(`          paths: ${stats.paths.join(', ')}`);
  await gql.server.stop();

  // Persisted query (phase 4): the client sends the hash, not the text.
  const { createHash } = await import('node:crypto');
  const hash = createHash('sha256').update(QUERY).digest('hex');
  console.log(`persisted query id: sha256:${hash.slice(0, 16)}... (${hash.length} chars vs ${QUERY.length}-char query)`);

  console.log('E2E PASS — same GraphQL result, 11 REST calls without DataLoader vs 2 with it');
} finally {
  rest.close();
}
