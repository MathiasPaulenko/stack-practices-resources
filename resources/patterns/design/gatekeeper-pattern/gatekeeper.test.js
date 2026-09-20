const { test } = require('node:test');
const assert = require('node:assert/strict');
const { Gatekeeper, signJwt, JWT_SECRET } = require('./gatekeeper.js');
const { buildApp } = require('./express_app.js');

const validToken = () =>
  signJwt({ sub: 'user-1', exp: Math.floor(Date.now() / 1000) + 3600 });
const authed = (path = '/api/orders') => ({
  path,
  headers: { Authorization: `Bearer ${validToken()}` },
});

// --- Gatekeeper class ---

test('blocked path rejected before auth', () => {
  const d = new Gatekeeper().inspect(authed('/admin/panel'));
  assert.equal(d.allowed, false);
  assert.equal(d.status, 403);
});

test('injection in query rejected', () => {
  const d = new Gatekeeper().inspect({ path: '/api/orders', query: 'id=1 or 1=1' });
  assert.equal(d.allowed, false);
  assert.equal(d.status, 400);
});

test('rate limit kicks in', () => {
  const gk = new Gatekeeper({ rateLimit: 3 });
  const req = { path: '/api/public/products', clientIp: '10.0.0.9' };
  for (let i = 0; i < 3; i++) assert.equal(gk.inspect(req).allowed, true);
  assert.equal(gk.inspect(req).status, 429);
});

test('missing token rejected on protected route', () => {
  const d = new Gatekeeper().inspect({ path: '/api/orders' });
  assert.equal(d.status, 401);
});

test('expired and forged tokens rejected', () => {
  const gk = new Gatekeeper();
  const expired = signJwt({ sub: 'u', exp: Math.floor(Date.now() / 1000) - 10 });
  const forged = signJwt({ sub: 'u', exp: Math.floor(Date.now() / 1000) + 60 }, 'wrong-secret');
  for (const token of [expired, forged]) {
    const d = gk.inspect({ path: '/api/orders', headers: { Authorization: `Bearer ${token}` } });
    assert.equal(d.allowed, false);
  }
});

test('valid token passes and exposes user', () => {
  const req = authed();
  const d = new Gatekeeper().inspect(req);
  assert.equal(d.allowed, true);
  assert.equal(d.user.sub, 'user-1');
});

test('public route skips auth but not other layers', () => {
  const gk = new Gatekeeper();
  assert.equal(gk.inspect({ path: '/api/public/products' }).allowed, true);
  assert.equal(
    gk.inspect({ path: '/api/public/products', query: "q=';drop table users--" }).allowed,
    false
  );
});

// --- Express-style middleware stack ---

function fakeRes() {
  const res = {
    statusCode: 200,
    body: null,
    status(code) {
      this.statusCode = code;
      return this;
    },
    json(obj) {
      this.body = obj;
    },
    end() {},
  };
  return res;
}

test('middleware stack rejects blocked path with 403', () => {
  const res = fakeRes();
  buildApp().handle({ path: '/admin/x', method: 'GET' }, res);
  assert.equal(res.statusCode, 403);
  assert.equal(res.body.code, 'BLOCKED_PATH');
});

test('middleware stack passes valid token to handler', () => {
  const res = fakeRes();
  buildApp().handle(
    { path: '/api/protected/users/me', method: 'GET', headers: { Authorization: `Bearer ${validToken()}` } },
    res
  );
  assert.equal(res.statusCode, 200);
  assert.equal(res.body.userId, 'user-1');
});

test('public route reachable without a token through the stack', () => {
  const res = fakeRes();
  buildApp().handle({ path: '/api/public/products', method: 'GET', headers: {} }, res);
  assert.equal(res.statusCode, 200);
});
