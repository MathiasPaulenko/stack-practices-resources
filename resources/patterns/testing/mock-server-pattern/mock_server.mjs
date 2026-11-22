/**
 * Mock Server Pattern — runnable Node.js companion (zero dependencies).
 *
 * A real HTTP mock server on a random port: register stubs per test,
 * record every incoming request, verify afterwards. Same lifecycle as
 * WireMock/nock/MSW — configure, intercept, match, verify.
 *
 * Run: node mock_server.mjs
 * Tests: node --test mock_server.mjs
 */

import http from 'node:http';
import test from 'node:test';
import assert from 'node:assert/strict';

class MockServer {
  constructor() {
    this.stubs = [];
    this.requests = [];
    this.server = http.createServer((req, res) => this._handle(req, res));
  }

  stub(method, path, { status = 200, body = null, headers = {} } = {}) {
    this.stubs.push({ method: method.toUpperCase(), path, status, body, headers });
    return this;
  }

  reset() {
    this.stubs = [];
    this.requests = [];
  }

  verify(method, path) {
    return this.requests.some(
      (r) => r.method === method.toUpperCase() && r.path === path,
    );
  }

  _handle(req, res) {
    const chunks = [];
    req.on('data', (c) => chunks.push(c));
    req.on('end', () => {
      this.requests.push({
        method: req.method,
        path: req.url,
        body: Buffer.concat(chunks).toString(),
      });
      const stub = this.stubs.find(
        (s) => s.method === req.method && s.path === req.url,
      );
      if (!stub) {
        res.writeHead(404, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: 'no stub matched' }));
        return;
      }
      res.writeHead(stub.status, {
        'Content-Type': 'application/json',
        ...stub.headers,
      });
      res.end(stub.body === null ? '' : JSON.stringify(stub.body));
    });
  }

  listen() {
    return new Promise((resolve) => {
      this.server.listen(0, '127.0.0.1', () => {
        this.url = `http://127.0.0.1:${this.server.address().port}`;
        resolve(this.url);
      });
    });
  }

  close() {
    return new Promise((resolve) => this.server.close(resolve));
  }
}

class NotFoundError extends Error {}

class UserService {
  constructor(baseUrl) {
    this.baseUrl = baseUrl;
  }

  async getUser(id) {
    const res = await fetch(`${this.baseUrl}/users/${id}`);
    if (res.status === 404) throw new NotFoundError(`user ${id}`);
    return res.json();
  }
}

// --- tests ---------------------------------------------------------------

test('mock server lifecycle', async (t) => {
  const mock = new MockServer();
  await mock.listen();
  const client = new UserService(mock.url);
  t.after(async () => {
    await mock.close();
  });

  await t.test('returns the stubbed response over a real socket', async () => {
    mock.stub('GET', '/users/1', {
      body: { id: 1, name: 'Alice', email: 'alice@x.com' },
    });
    const user = await client.getUser(1);
    assert.equal(user.name, 'Alice');
  });

  await t.test('propagates stubbed errors to the client', async () => {
    mock.stub('GET', '/users/999', { status: 404 });
    await assert.rejects(() => client.getUser(999), NotFoundError);
  });

  await t.test('unstubbed paths 404 by default', async () => {
    await assert.rejects(() => client.getUser(42), NotFoundError);
  });

  await t.test('verify() confirms the request was made', async () => {
    mock.stub('GET', '/users/1', { body: { id: 1 } });
    await client.getUser(1);
    assert.ok(mock.verify('GET', '/users/1'));
    assert.ok(!mock.verify('POST', '/users'));
  });

  await t.test('reset() clears stubs and recorded requests', async () => {
    mock.stub('GET', '/users/1', { body: { id: 1 } });
    await client.getUser(1);
    mock.reset();
    assert.ok(!mock.verify('GET', '/users/1'));
    await assert.rejects(() => client.getUser(1), NotFoundError);
  });
});

// --- demo when run directly ----------------------------------------------

if (process.argv[1] && process.argv[1].endsWith('mock_server.mjs')
    && !process.argv.includes('--test')) {
  const mock = new MockServer();
  await mock.listen();
  mock.stub('GET', '/users/1', {
    body: { id: 1, name: 'Alice', email: 'alice@x.com' },
  });
  const user = await new UserService(mock.url).getUser(1);
  console.log(`Mock server on ${mock.url} answered:`, user);
  await mock.close();
}
