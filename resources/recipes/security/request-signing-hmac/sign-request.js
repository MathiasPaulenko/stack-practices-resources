// HMAC-SHA256 request signing — sign and verify.
const crypto = require('crypto');

function signRequest(secret, method, path, body = '') {
  const timestamp = new Date().toISOString();
  const message = `${method}\n${path}\n${timestamp}\n${body}`;

  const signature = crypto
    .createHmac('sha256', secret)
    .update(message)
    .digest('hex');

  return {
    'X-Request-Timestamp': timestamp,
    'X-Request-Signature': signature,
  };
}

// Server verification. timingSafeEqual throws when buffer lengths
// differ, so the length check has to come first — a missing or
// truncated signature would otherwise turn into an unhandled 500.
function verifyRequest(secret, headers, method, path, body) {
  const provided = headers['x-request-signature'];
  if (typeof provided !== 'string') return false;

  const expected = signRequest(secret, method, path, body)['X-Request-Signature'];
  const providedBuf = Buffer.from(provided);
  const expectedBuf = Buffer.from(expected);

  return providedBuf.length === expectedBuf.length
    && crypto.timingSafeEqual(providedBuf, expectedBuf);
}

// Round-trip demo
const headers = signRequest('my-secret-key', 'POST', '/api/orders', '{"item": "book"}');
console.log('signature verifies:', verifyRequest(
  'my-secret-key', headers, 'POST', '/api/orders', '{"item": "book"}'
));

module.exports = { signRequest, verifyRequest };
