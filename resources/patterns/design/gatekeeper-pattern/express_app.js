/**
 * Gatekeeper in the wild — an Express-style middleware stack.
 *
 * Express middleware is where this pattern hides in plain sight: each
 * `app.use()` stage gets one shot at the request, and a stage that never
 * calls next() is the gatekeeper rejecting at the edge.
 *
 * This file ships its own minimal middleware engine so the example runs
 * with zero dependencies. The same functions drop straight into real
 * Express — swap `createApp()` for `express()` and they work unchanged.
 *
 * Run:  node express_app.js   (starts the server on :3000)
 * Test: node --test gatekeeper.test.js
 */

const { Gatekeeper } = require('./gatekeeper.js');

/** Minimal (req, res, next) engine replicating Express semantics. */
function createApp() {
  const stack = [];
  const app = {
    use: (prefix, fn) => stack.push({ prefix: fn ? prefix : '/', fn: fn || prefix }),
    get: (path, fn) => stack.push({ prefix: path, fn, method: 'GET' }),
    handle(req, res) {
      let i = 0;
      const next = () => {
        const layer = stack[i++];
        if (!layer) return res.end();
        if (layer.method && layer.method !== req.method) return next();
        if (!req.path.startsWith(layer.prefix)) return next();
        layer.fn(req, res, next);
      };
      next();
    },
  };
  return app;
}

function buildApp(gatekeeper = new Gatekeeper()) {
  const app = createApp();

  // One middleware per gatekeeper layer — same order as Gatekeeper.inspect().
  app.use((req, res, next) => {
    const rejection = gatekeeper.checkPath(req);
    if (rejection) return res.status(rejection.status).json({ error: rejection.reason, code: rejection.code });
    next();
  });

  app.use((req, res, next) => {
    const rejection = gatekeeper.checkRate(req);
    if (rejection) return res.status(rejection.status).json({ error: rejection.reason, code: rejection.code });
    next();
  });

  app.use((req, res, next) => {
    const rejection = gatekeeper.checkInjection(req);
    if (rejection) return res.status(rejection.status).json({ error: rejection.reason, code: rejection.code });
    next();
  });

  app.use((req, res, next) => {
    const rejection = gatekeeper.checkAuth(req); // sets req.user on success
    if (rejection) return res.status(rejection.status).json({ error: rejection.reason, code: rejection.code });
    next();
  });

  // Backend routes — public and protected are explicit.
  app.get('/api/public/products', (req, res) => {
    res.json({ products: [{ id: 1, name: 'Widget' }] });
  });

  app.get('/api/protected/users/me', (req, res) => {
    res.json({ userId: req.user.sub });
  });

  return app;
}

if (require.main === module) {
  const http = require('node:http');
  const app = buildApp();
  http
    .createServer((req, res) => {
      const url = new URL(req.url, 'http://localhost');
      const headers = {};
      res.status = (code) => (res.statusCode = code, res);
      res.json = (body) => res.end(JSON.stringify(body));
      app.handle(
        { path: url.pathname, query: url.search.slice(1), headers: req.headers, method: req.method, clientIp: req.socket.remoteAddress },
        res
      );
    })
    .listen(3000, () => console.log('Gatekeeper listening on :3000'));
}

module.exports = { buildApp, createApp };
