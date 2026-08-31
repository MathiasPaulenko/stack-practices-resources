const crypto = require('crypto');

const ITERATIONS = 600_000;
const KEYLEN = 32;
const DIGEST = 'sha256';

function hashPassword(password) {
  const salt = crypto.randomBytes(16);
  const key = crypto.pbkdf2Sync(password, salt, ITERATIONS, KEYLEN, DIGEST);
  return `pbkdf2_sha256$${ITERATIONS}$${salt.toString('hex')}$${key.toString('hex')}`;
}

function verifyPassword(stored, password) {
  const [_, iters, saltHex, hashHex] = stored.split('$');
  const salt = Buffer.from(saltHex, 'hex');
  const expected = Buffer.from(hashHex, 'hex');
  const derived = crypto.pbkdf2Sync(password, salt, parseInt(iters, 10), expected.length, DIGEST);
  return crypto.timingSafeEqual(derived, expected);
}

const password = 'supersecret';
const start = Date.now();
const stored = hashPassword(password);
const hashMs = Date.now() - start;
console.log(`PBKDF2 stored: ${stored}`);
console.log(`hash time: ${hashMs} ms`);
console.log(`verify: ${verifyPassword(stored, password)}`);
