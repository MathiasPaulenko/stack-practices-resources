// csrf-middleware.js — signed double-submit CSRF protection for Express.
// Usage:
//   const { csrfProtection } = require('./csrf-middleware');
//   app.use(csrfProtection());
// Requires: cookie-parser. Set CSRF_SECRET in the environment.
const crypto = require('crypto');

const CSRF_SECRET = process.env.CSRF_SECRET;
if (!CSRF_SECRET) {
  throw new Error('CSRF_SECRET env var is required');
}

function tokensEqual(a, b) {
  // timingSafeEqual throws on length mismatch — guard first so a forged
  // cookie produces a clean 403 instead of an unhandled 500.
  const ba = Buffer.from(a);
  const bb = Buffer.from(b);
  return ba.length === bb.length && crypto.timingSafeEqual(ba, bb);
}

function signToken(token) {
  return crypto.createHmac('sha256', CSRF_SECRET).update(token).digest('hex');
}

function issueToken(res) {
  const token = crypto.randomBytes(32).toString('hex');
  const signature = signToken(token);
  // httpOnly:false on purpose — the client must read this cookie and echo
  // the token back in the X-CSRF-Token header (double-submit pattern).
  res.cookie('csrfToken', `${token}.${signature}`, {
    httpOnly: false,
    secure: true,
    sameSite: 'strict',
  });
  return token;
}

function csrfProtection(options = {}) {
  const safeMethods = new Set(['GET', 'HEAD', 'OPTIONS']);
  const ignorePaths = new Set(options.ignorePaths || []);

  return function middleware(req, res, next) {
    if (safeMethods.has(req.method) || ignorePaths.has(req.path)) {
      // Make sure a token exists so SPAs can read it on first load.
      if (!req.cookies.csrfToken) issueToken(res);
      return next();
    }

    const headerToken = req.headers['x-csrf-token'];
    const cookieToken = req.cookies.csrfToken;
    if (!headerToken || !cookieToken) {
      return res.status(403).json({ error: 'CSRF token missing' });
    }

    const [tokenValue, signature] = cookieToken.split('.');
    const validSignature = tokensEqual(signature || '', signToken(tokenValue || ''));
    const validToken = tokensEqual(headerToken, tokenValue || '');

    if (!validSignature || !validToken) {
      return res.status(403).json({ error: 'Invalid CSRF token' });
    }
    next();
  };
}

module.exports = { csrfProtection, issueToken };
