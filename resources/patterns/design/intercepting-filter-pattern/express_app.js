/**
 * Intercepting Filter in the wild — Express middleware.
 *
 * Express middleware IS this pattern: each middleware gets (req, res, next)
 * and calling next() delegates to the next filter in the chain.
 *
 * Run:      node express_app.js   (starts the server on :3000)
 * Test:     npm test              (uses node:test + node:assert)
 */

function createApp() {
  // Minimal middleware engine replicating Express semantics.
  const chain = [];
  const app = {
    use: (fn) => chain.push(fn),
    handle(req, res) {
      let i = 0;
      const next = (err) => {
        if (err) return res.end(JSON.stringify({ error: err.message }));
        const mw = chain[i++];
        if (!mw) return;
        mw(req, res, next);
      };
      next();
    },
  };
  return app;
}

// --- Intercepting Filters as Express-style middleware ---

const requestLogger = (req, res, next) => {
  console.log(`[LOG] -> ${req.method} ${req.url}`);
  res.onFinish = () => console.log(`[LOG] <- ${res.statusCode}`);
  next();
};

const authenticate = (req, res, next) => {
  const token = req.headers['authorization'];
  if (token && token.startsWith('Bearer ')) {
    req.user = 'authenticated_user';
    return next();
  }
  res.statusCode = 401;
  res.end(JSON.stringify({ error: 'Unauthorized' })); // short-circuit
};

const gzipHeader = (req, res, next) => {
  const end = res.end.bind(res);
  res.end = (body) => {
    if ((req.headers['accept-encoding'] || '').includes('gzip')) {
      res.setHeader('Content-Encoding', 'gzip');
    }
    res.onFinish && res.onFinish();
    end(body);
  };
  next();
};

const helloHandler = (req, res) => {
  res.statusCode = 200;
  res.setHeader('Content-Type', 'application/json');
  res.end(JSON.stringify({ message: `Hello, ${req.user || 'guest'}!` }));
};

function buildApp() {
  const app = createApp();
  app.use(requestLogger);
  app.use(authenticate);
  app.use(gzipHeader);
  app.use(helloHandler);
  return app;
}

module.exports = { createApp, buildApp, requestLogger, authenticate, gzipHeader, helloHandler };

if (require.main === module) {
  const http = require('http');
  const app = buildApp();
  http
    .createServer((req, res) => app.handle(req, res))
    .listen(3000, () => console.log('http://localhost:3000/api/hello'));
}
