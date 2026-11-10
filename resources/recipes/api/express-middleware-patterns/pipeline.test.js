// Integration tests for the middleware pipeline — node:test + fetch, no deps.
import { test, before, after } from 'node:test';
import assert from 'node:assert/strict';
import { createServer } from 'node:http';
import { routes } from './middleware_pipeline.js';

let server, base;

before(async () => {
  server = createServer(routes).listen(0);
  await new Promise((r) => server.once('listening', r));
  base = `http://localhost:${server.address().port}`;
});

after(() => server.close());

test('GET /users/1 returns user with trace id', async () => {
  const res = await fetch(`${base}/users/1`);
  assert.equal(res.status, 200);
  const body = await res.json();
  assert.equal(body.user.name, 'Alice');
  assert.ok(body.traceId);
});

test('trace id from request header is echoed back', async () => {
  const res = await fetch(`${base}/users/1`, { headers: { 'X-Trace-Id': 'trace-42' } });
  assert.equal(res.headers.get('x-trace-id'), 'trace-42');
});

test('POST /users without auth returns 403 AppError', async () => {
  const res = await fetch(`${base}/users`, { method: 'POST', body: '{"name":"Bob"}' });
  assert.equal(res.status, 403);
  assert.equal((await res.json()).code, 'FORBIDDEN');
});

test('POST /users with invalid body returns 400', async () => {
  const res = await fetch(`${base}/users`, {
    method: 'POST',
    headers: { authorization: 'Bearer demo' },
    body: '{"name": 42}',
  });
  assert.equal(res.status, 400);
  assert.equal((await res.json()).code, 'VALIDATION');
});

test('unhandled rejection in handler returns 500 with traceId', async () => {
  const res = await fetch(`${base}/boom`, { headers: { 'X-Trace-Id': 't-500' } });
  assert.equal(res.status, 500);
  assert.equal((await res.json()).traceId, 't-500');
});
