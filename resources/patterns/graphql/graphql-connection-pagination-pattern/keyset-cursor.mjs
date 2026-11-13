// Keyset (sort-key) cursor: jumps to position via an indexed predicate
// instead of scanning OFFSET rows. Same connection shape, better at scale.
// Run: node keyset-cursor.mjs — no dependencies.

import { createDb } from './mock-db.mjs';

const base64 = (s) => Buffer.from(s).toString('base64');
const unbase64 = (s) => Buffer.from(s, 'base64').toString('utf8');

const encodeCursor = (sortKey, id) => base64(`${sortKey}:${id}`);
const decodeCursor = (cursor) => {
  const [sortKey, id] = unbase64(cursor).split(':');
  return { sortKey, id };
};

function createUsersResolver(db) {
  return async function users({ first, after } = {}) {
    const limit = Math.min(first || 20, 100);

    let createdAt = null;
    let id = null;
    if (after) {
      const decoded = decodeCursor(after);
      createdAt = decoded.sortKey;
      id = decoded.id;
    }

    // WHERE (created_at, id) < ($1, $2) ORDER BY created_at DESC, id DESC
    const rows = await db.queryKeyset(createdAt, id, limit + 1);
    const hasMore = rows.length > limit;
    const nodes = hasMore ? rows.slice(0, limit) : rows;

    const edges = nodes.map((node) => ({
      node,
      cursor: encodeCursor(node.created_at, node.id),
    }));

    return {
      edges,
      pageInfo: {
        hasNextPage: hasMore,
        hasPreviousPage: after != null,
        startCursor: edges[0]?.cursor ?? null,
        endCursor: edges[edges.length - 1]?.cursor ?? null,
      },
    };
  };
}

// Demo: same walk as offset-cursor, but the cursor carries (created_at, id)
// so the database can seek with an index instead of counting rows to skip.
const db = createDb();
const users = createUsersResolver(db);

let after = null;
let page = 0;
let conn;
while (true) {
  conn = await users({ first: 20, after });
  page += 1;
  console.log(
    `Page ${page}: ${conn.edges.length} edges, ` +
      `hasNextPage=${conn.pageInfo.hasNextPage}, ` +
      `endCursor=${conn.pageInfo.endCursor?.slice(0, 32)}...`
  );
  if (!conn.pageInfo.hasNextPage) break;
  after = conn.pageInfo.endCursor;
}
console.log(`${page} pages, ${db.queryCount} queries — one indexed seek per page`);
