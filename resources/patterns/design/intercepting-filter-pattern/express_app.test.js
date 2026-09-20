const { test } = require('node:test');
const assert = require('node:assert/strict');
const { buildApp } = require('./express_app.js');
const { buildChain, HttpRequest, HttpResponse } = require('./filter_chain.js');

// --- Plain chain ---

test('authenticated request reaches the target', () => {
  const chain = buildChain();
  const req = new HttpRequest('/api/hello', { Authorization: 'Bearer abc' });
  const res = new HttpResponse();
  chain.execute(req, res);
  assert.equal(res.status, 200);
  assert.deepEqual(res.body, { message: 'Hello, authenticated_user!' });
});

test('missing token short-circuits with 401', () => {
  const chain = buildChain();
  const res = new HttpResponse();
  chain.execute(new HttpRequest('/api/hello', {}), res);
  assert.equal(res.status, 401);
  assert.deepEqual(res.body, { error: 'Unauthorized' });
});

test('gzip accept gets Content-Encoding header', () => {
  const chain = buildChain();
  const req = new HttpRequest('/api/hello', {
    Authorization: 'Bearer abc',
    'Accept-Encoding': 'gzip',
  });
  const res = new HttpResponse();
  chain.execute(req, res);
  assert.equal(res.headers['Content-Encoding'], 'gzip');
});

test('the same chain instance serves consecutive requests', () => {
  const chain = buildChain();
  const a = new HttpResponse();
  const b = new HttpResponse();
  chain.execute(new HttpRequest('/x', { Authorization: 'Bearer t' }), a);
  chain.execute(new HttpRequest('/x', { Authorization: 'Bearer t' }), b);
  assert.equal(a.status, 200);
  assert.equal(b.status, 200);
});

// --- Express-style middleware app ---

function fakeReq(headers = {}) {
  return { method: 'GET', url: '/api/hello', headers };
}

function fakeRes() {
  return {
    statusCode: 200,
    headers: {},
    setHeader(k, v) { this.headers[k] = v; },
    end(body) { this.body = body; },
  };
}

test('express pipeline: unauthenticated request gets 401', () => {
  const app = buildApp();
  const res = fakeRes();
  app.handle(fakeReq(), res);
  assert.equal(res.statusCode, 401);
  assert.deepEqual(JSON.parse(res.body), { error: 'Unauthorized' });
});

test('express pipeline: authenticated request gets greeting + gzip', () => {
  const app = buildApp();
  const res = fakeRes();
  app.handle(fakeReq({ authorization: 'Bearer abc', 'accept-encoding': 'gzip' }), res);
  assert.equal(res.statusCode, 200);
  assert.equal(res.headers['Content-Encoding'], 'gzip');
  assert.deepEqual(JSON.parse(res.body), { message: 'Hello, authenticated_user!' });
});
