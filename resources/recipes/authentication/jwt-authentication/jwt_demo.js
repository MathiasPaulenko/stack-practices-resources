// Runnable JWT demo for Node.js.
//   npm install
//   node jwt_demo.js
const jwt = require('jsonwebtoken');
const crypto = require('crypto');

const SECRET = process.env.JWT_SECRET || 'dev-only-secret-change-me-0123456789';
const REFRESH_TTL_DAYS = 7;

const refreshStore = new Map();
const blocklist = new Set();

function createAccessToken(userId) {
  return jwt.sign(
    { sub: userId, type: 'access' },
    SECRET,
    { expiresIn: '15m' }
  );
}

function createRefreshToken(userId) {
  const jti = crypto.randomBytes(32).toString('hex');
  const token = jwt.sign(
    { sub: userId, type: 'refresh', jti },
    SECRET,
    { expiresIn: `${REFRESH_TTL_DAYS}d` }
  );
  refreshStore.set(jti, userId);
  return token;
}

function verify(token, expectedType = 'access') {
  const claims = jwt.verify(token, SECRET);
  if (claims.type !== expectedType) throw new Error(`Not a ${expectedType} token`);
  if (claims.jti && blocklist.has(claims.jti)) throw new Error('Token has been revoked');
  return claims;
}

function refreshAccessToken(refreshToken) {
  const claims = verify(refreshToken, 'refresh');
  if (!refreshStore.has(claims.jti)) throw new Error('Refresh token has been revoked');
  return createAccessToken(claims.sub);
}

function revokeRefreshToken(refreshToken) {
  const claims = jwt.verify(refreshToken, SECRET);
  refreshStore.delete(claims.jti);
  blocklist.add(claims.jti);
}

const access = createAccessToken('user-123');
const refresh = createRefreshToken('user-123');

console.log('access token ok, sub =', verify(access).sub);
console.log('refresh flow ok:', refreshAccessToken(refresh).slice(0, 30) + '...');

revokeRefreshToken(refresh);
try {
  refreshAccessToken(refresh);
  console.log('ERROR: revoked refresh token still works');
} catch (e) {
  console.log('revocation ok:', e.message);
}
