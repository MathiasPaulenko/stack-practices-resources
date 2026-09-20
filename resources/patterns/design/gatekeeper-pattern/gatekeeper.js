/**
 * Gatekeeper pattern — a framework-free edge validator.
 *
 * One inspection point in front of the services: blocked paths, rate
 * limiting, injection screening, and JWT authentication — in that order.
 * Public routes (`/api/public/*`, `/health`) skip authentication but
 * still go through every other layer.
 *
 * Run the demo:   node gatekeeper.js
 * Run the tests:  node --test gatekeeper.test.js
 */

const crypto = require('node:crypto');

// Fail fast if the secret is missing — never ship a fallback secret.
const JWT_SECRET = process.env.GATEKEEPER_JWT_SECRET || 'dev-secret-for-demo-only';

const b64urlEncode = (buf) => Buffer.from(buf).toString('base64url');
const b64urlDecode = (str) => Buffer.from(str, 'base64url');

function signJwt(payload, secret = JWT_SECRET) {
  const header = b64urlEncode(JSON.stringify({ alg: 'HS256', typ: 'JWT' }));
  const body = b64urlEncode(JSON.stringify(payload));
  const sig = crypto
    .createHmac('sha256', secret)
    .update(`${header}.${body}`)
    .digest();
  return `${header}.${body}.${b64urlEncode(sig)}`;
}

function verifyJwt(token, secret = JWT_SECRET) {
  const parts = token.split('.');
  if (parts.length !== 3) return null;
  const [header, body, sig] = parts;
  const expected = crypto
    .createHmac('sha256', secret)
    .update(`${header}.${body}`)
    .digest();
  const actual = b64urlDecode(sig);
  if (actual.length !== expected.length || !crypto.timingSafeEqual(actual, expected)) {
    return null;
  }
  const payload = JSON.parse(b64urlDecode(body).toString());
  if (payload.exp && payload.exp < Date.now() / 1000) return null;
  return payload;
}

class Gatekeeper {
  static BLOCKED_PATHS = ['/admin', '/internal', '/debug', '/.env', '/wp-admin'];
  static PUBLIC_PREFIXES = ['/api/public', '/health'];
  static INJECTION_PATTERNS = [
    /\b(union|select|insert|update|delete|drop)\b/i,
    /(--|;|\/\*|\*\/)/,
    /\b(or|and)\b\s+\d+\s*=\s*\d+/i,
  ];

  constructor({ rateLimit = 100, windowMs = 60_000 } = {}) {
    this.rateLimit = rateLimit;
    this.windowMs = windowMs;
    // In production this lives in Redis so replicas share counters.
    this.hits = new Map();
  }

  // Each check returns a rejection decision or null when the layer passes,
  // so middleware stacks can run the layers individually.
  checkPath(req) {
    if (Gatekeeper.BLOCKED_PATHS.some((p) => req.path.startsWith(p))) {
      return { allowed: false, status: 403, code: 'BLOCKED_PATH', reason: 'path is not public' };
    }
    return null;
  }

  checkRate(req) {
    if (this._overLimit(req.clientIp || 'unknown')) {
      return { allowed: false, status: 429, code: 'RATE_LIMITED', reason: 'too many requests' };
    }
    return null;
  }

  checkInjection(req) {
    if (this._looksInjected(req)) {
      return { allowed: false, status: 400, code: 'INJECTION_DETECTED', reason: 'malformed input' };
    }
    return null;
  }

  checkAuth(req) {
    if (Gatekeeper.PUBLIC_PREFIXES.some((p) => req.path.startsWith(p))) {
      return null;
    }
    const auth = (req.headers || {}).Authorization || (req.headers || {}).authorization || '';
    if (!auth.startsWith('Bearer ')) {
      return { allowed: false, status: 401, code: 'AUTH_FAILED', reason: 'missing bearer token' };
    }
    const payload = verifyJwt(auth.slice(7));
    if (!payload) {
      return { allowed: false, status: 401, code: 'AUTH_FAILED', reason: 'invalid or expired token' };
    }
    // Attach the verified payload so downstream handlers can use it.
    req.user = payload;
    return null;
  }

  /** Runs every layer in order. Returns { allowed, status, code, reason, user? }. */
  inspect(req) {
    for (const check of [this.checkPath, this.checkRate, this.checkInjection, this.checkAuth]) {
      const rejection = check.call(this, req);
      if (rejection) return rejection;
    }
    return { allowed: true, status: 200, code: 'OK', user: req.user };
  }

  _overLimit(clientIp) {
    const now = Date.now();
    const hits = (this.hits.get(clientIp) || []).filter((t) => t > now - this.windowMs);
    if (hits.length >= this.rateLimit) {
      this.hits.set(clientIp, hits);
      return true;
    }
    hits.push(now);
    this.hits.set(clientIp, hits);
    return false;
  }

  _looksInjected(req) {
    const target = `${req.path}?${req.query || ''}`;
    return Gatekeeper.INJECTION_PATTERNS.some((p) => p.test(target));
  }
}

if (require.main === module) {
  const gk = new Gatekeeper();
  const token = signJwt({ sub: 'user-1', exp: Math.floor(Date.now() / 1000) + 3600 });

  const cases = [
    { path: '/admin/panel' },
    { path: '/api/orders', query: 'id=1 or 1=1' },
    { path: '/api/orders' },
    { path: '/api/orders', headers: { Authorization: `Bearer ${token}` } },
    { path: '/api/public/products' },
    { path: '/api/protected/users/me', headers: { Authorization: `Bearer ${token}` } },
  ];
  for (const req of cases) {
    const d = gk.inspect(req);
    const verdict = d.allowed ? 'PASS' : `REJECT ${d.status}`;
    console.log(`${verdict.padStart(11)}  ${req.path}${req.query ? '?' + req.query : ''}  [${d.code}]`);
  }
}

module.exports = { Gatekeeper, signJwt, verifyJwt, JWT_SECRET };
