// The five middleware composition patterns on node:http — zero dependencies.
// The (req, res, next) contract mirrors Express, so each piece ports directly.

import { createServer } from 'node:http';
import { AsyncLocalStorage } from 'node:async_hooks';
import { randomUUID } from 'node:crypto';

// --- Pattern 4 (used by 1): unified error type --------------------------------
class AppError extends Error {
  constructor(statusCode, message, code) {
    super(message);
    this.statusCode = statusCode;
    this.code = code;
  }
}

// --- Pattern 3: request context propagation ----------------------------------
const storage = new AsyncLocalStorage();
const getContext = () => storage.getStore();

const contextMiddleware = (req, res, next) => {
  const ctx = { traceId: req.headers['x-trace-id'] || randomUUID(), start: Date.now() };
  storage.run(ctx, () => {
    res.setHeader('X-Trace-Id', ctx.traceId);
    next();
  });
};

// --- Pattern 1: async route wrapper ------------------------------------------
const asyncHandler = (fn) => (req, res, next) =>
  Promise.resolve(fn(req, res, next)).catch(next);

// --- Pattern 2: composable middleware factory --------------------------------
const compose = (...middlewares) => middlewares.flat();

// A tiny (req, res, next) pipeline runner — the part Express gives you for free.
function pipeline(middlewares, finalHandler) {
  return (req, res) => {
    const stack = [...middlewares];
    const next = (err) => {
      if (err) return errorHandler(err, req, res);
      const mw = stack.shift();
      if (!mw) return finalHandler(req, res, next);
      mw.length === 4 ? mw(err, req, res, next) : mw(req, res, next);
    };
    next();
  };
}

// --- Pattern 5: schema validation middleware ---------------------------------
const validateBody = (schema) => async (req, res, next) => {
  const chunks = [];
  for await (const c of req) chunks.push(c);
  let body;
  try {
    body = JSON.parse(Buffer.concat(chunks).toString() || '{}');
  } catch {
    return next(new AppError(400, 'Malformed JSON', 'BAD_JSON'));
  }
  const issues = Object.entries(schema)
    .filter(([k, t]) => typeof body[k] !== t)
    .map(([k, t]) => `${k}: expected ${t}, got ${typeof body[k]}`);
  if (issues.length) {
    return next(new AppError(400, 'Validation failed', 'VALIDATION'));
  }
  req.body = body;
  next();
};

// --- Unified error handler (pattern 4) ---------------------------------------
function errorHandler(err, req, res) {
  const ctx = getContext();
  const status = err instanceof AppError ? err.statusCode : 500;
  const payload = {
    error: err instanceof AppError ? err.message : 'Internal server error',
    code: err.code,
    traceId: ctx?.traceId,
  };
  res.writeHead(status, { 'Content-Type': 'application/json' }).end(JSON.stringify(payload));
}

// --- Fake auth + routes --------------------------------------------------------
const requireAuth = (req, res, next) => {
  if (req.headers.authorization !== 'Bearer demo') {
    return next(new AppError(403, 'Missing bearer token', 'FORBIDDEN'));
  }
  next();
};

const authenticated = compose(requireAuth);

const routes = pipeline(
  [contextMiddleware],
  asyncHandler(async (req, res) => {
    const ctx = getContext();
    if (req.method === 'GET' && req.url.startsWith('/users/')) {
      const user = { id: req.url.split('/')[2], name: 'Alice' };
      return res.writeHead(200, { 'Content-Type': 'application/json' })
        .end(JSON.stringify({ user, traceId: ctx.traceId }));
    }
    if (req.method === 'POST' && req.url === '/users') {
      return pipeline(authenticated, (r, s) => {
        // nested: auth first, then validation, then the handler
        pipeline([validateBody({ name: 'string' })], (r2, s2) => {
          s2.writeHead(201, { 'Content-Type': 'application/json' })
            .end(JSON.stringify({ created: r2.body.name }));
        })(r, s);
      })(req, res);
    }
    if (req.url === '/boom') throw new Error('unexpected!');
    res.writeHead(404).end();
  })
);

if (process.argv[1] === new URL(import.meta.url).pathname) {
  createServer(routes).listen(3000, () => console.log('listening on :3000'));
}

export { routes, compose, asyncHandler, AppError, getContext };
