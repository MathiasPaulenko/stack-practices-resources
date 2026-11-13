// Offset-cursor connection resolver: the simplest Relay-style pagination.
// Run: node offset-cursor.mjs — no dependencies.

import { createDb } from './mock-db.mjs';

const base64 = (s) => Buffer.from(s).toString('base64');
const unbase64 = (s) => Buffer.from(s, 'base64').toString('utf8');

const DEFAULT_PAGE_SIZE = 20;
const MAX_PAGE_SIZE = 100;

const encodeCursor = (offset) => base64(`offset:${offset}`);
const decodeCursor = (cursor) => {
  const offset = parseInt(unbase64(cursor).split(':')[1], 10);
  return Number.isNaN(offset) ? 0 : offset;
};

function createUsersResolver(db) {
  return async function users({ first, after, last, before } = {}) {
    const limit = Math.min(first || last || DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE);
    const direction = first !== undefined ? 'forward' : 'backward';

    let offset = 0;
    if (after) offset = decodeCursor(after) + 1;
    if (before) offset = Math.max(0, decodeCursor(before) - limit);

    const totalCount = await db.count();
    const rows = await db.queryOffset(limit + 1, offset); // LIMIT + 1 trick
    const hasMore = rows.length > limit;
    const nodes = hasMore ? rows.slice(0, limit) : rows;

    const edges = nodes.map((node, index) => ({
      node,
      cursor: encodeCursor(offset + index),
    }));

    return {
      edges,
      totalCount,
      pageInfo: {
        hasNextPage: direction === 'forward' ? hasMore : offset + limit < totalCount,
        hasPreviousPage: offset > 0,
        startCursor: edges[0]?.cursor ?? null,
        endCursor: edges[edges.length - 1]?.cursor ?? null,
      },
    };
  };
}

// Demo: paginate forward through 95 users in pages of 20.
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
      `endCursor=${conn.pageInfo.endCursor}`
  );
  if (!conn.pageInfo.hasNextPage) break;
  after = conn.pageInfo.endCursor;
}
console.log(`Total: ${conn.totalCount} users, ${page} pages, ${db.queryCount} queries`);
