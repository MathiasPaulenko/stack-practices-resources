// cursor_pagination.ts
// TypeScript implementation of cursor-based (keyset) pagination with PostgreSQL.
// Uses the `pg` driver and base64url cursor encoding.

import { Pool } from 'pg';
import { Buffer } from 'buffer';

interface CursorData {
  createdAt: string;
  id: string;
}

interface PageResult<T> {
  data: T[];
  nextCursor: string | null;
  prevCursor: string | null;
  hasMore: boolean;
}

interface Post {
  id: string;
  created_at: string;
  title: string;
  score: number;
}

function encodeCursor(data: CursorData): string {
  const json = JSON.stringify(data);
  return Buffer.from(json).toString('base64url');
}

function decodeCursor(cursor: string): CursorData {
  const json = Buffer.from(cursor, 'base64url').toString('utf8');
  return JSON.parse(json);
}

class PostRepository {
  constructor(private pool: Pool) {}

  async findPage(
    limit: number = 20,
    afterCursor?: string,
    beforeCursor?: string
  ): Promise<PageResult<Post>> {
    const client = await this.pool.connect();

    try {
      let query: string;
      let params: unknown[];

      if (afterCursor) {
        const { createdAt, id } = decodeCursor(afterCursor);
        query = `
          SELECT * FROM posts
          WHERE (created_at, id) < ($1, $2)
          ORDER BY created_at DESC, id DESC
          LIMIT $3
        `;
        params = [createdAt, id, limit + 1];
      } else if (beforeCursor) {
        const { createdAt, id } = decodeCursor(beforeCursor);
        query = `
          SELECT * FROM (
            SELECT * FROM posts
            WHERE (created_at, id) > ($1, $2)
            ORDER BY created_at ASC, id ASC
            LIMIT $3
          ) sub
          ORDER BY created_at DESC, id DESC
        `;
        params = [createdAt, id, limit + 1];
      } else {
        query = `
          SELECT * FROM posts
          ORDER BY created_at DESC, id DESC
          LIMIT $1
        `;
        params = [limit + 1];
      }

      const result = await client.query(query, params);
      const rows = result.rows;
      const hasMore = rows.length > limit;
      const data = hasMore ? rows.slice(0, limit) : rows;

      const nextCursor =
        hasMore && data.length > 0
          ? encodeCursor({
              createdAt: data[data.length - 1].created_at,
              id: data[data.length - 1].id,
            })
          : null;

      const prevCursor =
        data.length > 0
          ? encodeCursor({ createdAt: data[0].created_at, id: data[0].id })
          : null;

      return {
        data,
        nextCursor,
        prevCursor: afterCursor || (!beforeCursor && data.length > 0) ? prevCursor : null,
        hasMore,
      };
    } finally {
      client.release();
    }
  }
}

export { PostRepository, encodeCursor, decodeCursor };
export type { CursorData, PageResult, Post };
