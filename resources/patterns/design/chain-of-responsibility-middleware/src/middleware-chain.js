// Chain of Responsibility — middleware pipeline (runnable, no dependencies)
// Usage: node middleware-chain.js
//
// Simulates an HTTP request crossing auth -> rate limit -> validation -> logging
// before reaching the endpoint handler. Any link may short-circuit the chain.

class MiddlewareHandler {
  constructor() {
    this.next = null;
  }

  setNext(handler) {
    this.next = handler;
    return handler;
  }

  handle(req, next) {
    if (this.canHandle(req)) {
      this.process(req, () => {
        if (this.next) this.next.handle(req, next);
        else next();
      });
    } else if (this.next) {
      this.next.handle(req, next);
    } else {
      next();
    }
  }

  canHandle(_req) {
    throw new Error('canHandle() not implemented');
  }

  process(_req, _next) {
    throw new Error('process() not implemented');
  }
}

class AuthMiddleware extends MiddlewareHandler {
  canHandle() {
    return true;
  }

  process(req, next) {
    const token = (req.headers['authorization'] || '').replace('Bearer ', '');
    if (!token) throw new Error('401 Unauthorized');
    // Demo token check: real code verifies signature and expiry.
    req.user = { id: 'user123', roles: ['user'] };
    console.log('  auth        -> user', req.user.id);
    next();
  }
}

class RateLimitMiddleware extends MiddlewareHandler {
  constructor() {
    super();
    this.requests = new Map();
    this.windowMs = 60_000;
    this.maxRequests = 100;
  }

  canHandle() {
    return true;
  }

  process(req, next) {
    const clientId = req.headers['x-client-id'] || (req.user && req.user.id) || 'anonymous';
    const now = Date.now();
    const recent = (this.requests.get(clientId) || []).filter((t) => now - t < this.windowMs);
    if (recent.length >= this.maxRequests) throw new Error('429 Rate limit exceeded');
    recent.push(now);
    this.requests.set(clientId, recent);
    console.log('  rate limit  ->', recent.length + '/' + this.maxRequests, 'for', clientId);
    next();
  }
}

class ValidationMiddleware extends MiddlewareHandler {
  canHandle(req) {
    return req.method === 'POST' || req.method === 'PUT';
  }

  process(req, next) {
    if (!req.body || typeof req.body !== 'object') throw new Error('400 Invalid request body');
    console.log('  validation  -> body ok');
    next();
  }
}

class LoggingMiddleware extends MiddlewareHandler {
  canHandle() {
    return true;
  }

  process(req, next) {
    console.log('  logging     ->', new Date().toISOString(), req.method, req.path);
    next();
  }
}

// --- Demo -------------------------------------------------------------------

const auth = new AuthMiddleware();
const rateLimit = new RateLimitMiddleware();
const validation = new ValidationMiddleware();
const logging = new LoggingMiddleware();

auth.setNext(rateLimit).setNext(validation).setNext(logging);

function handleRequest(req) {
  try {
    auth.handle(req, () => console.log('  endpoint    -> 200 OK for', req.path));
  } catch (err) {
    console.log('  chain error ->', err.message);
  }
}

console.log('Request 1: authenticated POST (passes every link)');
handleRequest({
  headers: { authorization: 'Bearer demo-token', 'x-client-id': 'cli-1' },
  body: { name: 'order' },
  path: '/orders',
  method: 'POST',
});

console.log('\nRequest 2: missing token (auth short-circuits)');
handleRequest({
  headers: {},
  body: { name: 'order' },
  path: '/orders',
  method: 'POST',
});

console.log('\nRequest 3: GET skips validation but crosses auth/rate-limit/logging');
handleRequest({
  headers: { authorization: 'Bearer demo-token' },
  path: '/orders',
  method: 'GET',
});
