import { createServer } from 'node:http';

// Request counter: the whole point of the demo is proving how many
// REST calls each GraphQL query fans out into.
export const stats = { requests: 0, paths: [] };
export const resetStats = () => { stats.requests = 0; stats.paths = []; };

const db = {
  users: new Map([
    [42, { id: 42, name: 'Ada', email: 'ada@example.com' }],
    [7, { id: 7, name: 'Grace', email: 'grace@example.com' }],
  ]),
  posts: Array.from({ length: 10 }, (_, i) => ({
    id: i + 1,
    authorId: i % 2 ? 42 : 7,
    title: `Post ${i + 1}`,
    createdAt: `2026-01-0${(i % 9) + 1}`,
  })),
};

const commentsFor = (postId) => [
  { id: postId * 10 + 1, body: `Comment on ${postId}` },
  { id: postId * 10 + 2, body: 'Nice post' },
];

export function startRestServer(port = 4001) {
  const server = createServer((req, res) => {
    stats.requests += 1;
    stats.paths.push(req.url);
    const url = new URL(req.url, `http://localhost:${port}`);
    const parts = url.pathname.split('/').filter(Boolean);
    let body = null;
    if (parts[0] === 'users' && parts.length === 1) {
      const ids = (url.searchParams.get('ids') ?? '')
        .split(',').map(Number).filter(Boolean);
      body = ids.map((id) => db.users.get(id)).filter(Boolean);
    } else if (parts[0] === 'users') {
      body = db.users.get(Number(parts[1])) ?? null;
    } else if (parts[0] === 'posts' && parts.length === 1) {
      body = db.posts.slice(0, Number(url.searchParams.get('limit') ?? 10));
    } else if (parts[0] === 'posts' && parts[2] === 'comments') {
      body = commentsFor(Number(parts[1]));
    } else if (parts[0] === 'posts') {
      body = db.posts.find((p) => p.id === Number(parts[1])) ?? null;
    }
    res.setHeader('content-type', 'application/json');
    res.end(JSON.stringify(body));
  });
  return new Promise((resolve) => server.listen(port, () => resolve(server)));
}
