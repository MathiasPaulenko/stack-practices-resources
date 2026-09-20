/**
 * totp-service.js — TOTP enrollment + verification service (Node/Express-ready).
 *
 * Same three pieces as the Python version:
 *   enroll()  → secret + provisioning URI + QR data-url
 *   confirm() → verify first code before enabling
 *   verify()  → login-time check with attempt limiting + backup codes
 *
 * Deps: npm install otplib qrcode
 *
 * Secrets are encrypted at rest with AES-256-GCM using a key from the
 * environment (TOTP_ENCRYPTION_KEY, 32-byte hex). Never store plaintext.
 */

const { authenticator } = require('otplib');
const QRCode = require('qrcode');
const crypto = require('crypto');

const MAX_ATTEMPTS = 5;
const ATTEMPT_WINDOW_MS = 5 * 60 * 1000;

class TOTPService {
  constructor(issuer = 'MyApp') {
    this.issuer = issuer;
    const keyHex = process.env.TOTP_ENCRYPTION_KEY;
    // Demo fallback — production MUST supply a 32-byte key via env/KMS
    this.key = keyHex ? Buffer.from(keyHex, 'hex') : crypto.randomBytes(32);
    this.users = new Map(); // userId -> { encryptedSecret, pendingSecret, enabled, backupHashes, attempts }
  }

  _user(userId) {
    if (!this.users.has(userId)) {
      this.users.set(userId, { enabled: false, backupHashes: new Set(), attempts: [] });
    }
    return this.users.get(userId);
  }

  _encrypt(plaintext) {
    const iv = crypto.randomBytes(12);
    const cipher = crypto.createCipheriv('aes-256-gcm', this.key, iv);
    const enc = Buffer.concat([cipher.update(plaintext, 'utf8'), cipher.final()]);
    return Buffer.concat([iv, cipher.getAuthTag(), enc]).toString('base64');
  }

  _decrypt(payload) {
    const raw = Buffer.from(payload, 'base64');
    const decipher = crypto.createDecipheriv('aes-256-gcm', this.key, raw.subarray(0, 12));
    decipher.setAuthTag(raw.subarray(12, 28));
    return Buffer.concat([decipher.update(raw.subarray(28)), decipher.final()]).toString('utf8');
  }

  _hash(code) {
    return crypto.createHash('sha256').update(code).digest('hex');
  }

  // ---------- enrollment ----------

  async enroll(userId, email) {
    const secret = authenticator.generateSecret();
    const uri = authenticator.keyuri(email, this.issuer, secret);
    const qrDataUrl = await QRCode.toDataURL(uri);
    this._user(userId).pendingSecret = this._encrypt(secret);
    return { provisioningUri: uri, qrDataUrl };
  }

  confirm(userId, token) {
    const u = this._user(userId);
    if (!u.pendingSecret) throw new Error('no pending enrollment');
    const secret = this._decrypt(u.pendingSecret);
    if (!authenticator.verify({ token, secret, window: 1 })) {
      return { enabled: false };
    }
    u.encryptedSecret = u.pendingSecret;
    u.pendingSecret = null;
    u.enabled = true;
    const codes = Array.from({ length: 10 }, () =>
      crypto.randomBytes(4).toString('hex').toUpperCase()
    );
    u.backupHashes = new Set(codes.map((c) => this._hash(c)));
    return { enabled: true, backupCodes: codes }; // show ONCE
  }

  // ---------- verification ----------

  verify(userId, token) {
    const u = this._user(userId);
    if (!u.enabled) throw new Error('2FA not enabled');

    const now = Date.now();
    u.attempts = u.attempts.filter((t) => now - t < ATTEMPT_WINDOW_MS);
    if (u.attempts.length >= MAX_ATTEMPTS) return false; // endpoint returns 429
    u.attempts.push(now);

    const hashed = this._hash(token.trim().toUpperCase());
    if (u.backupHashes.has(hashed)) {
      u.backupHashes.delete(hashed); // single-use
      return true;
    }

    const secret = this._decrypt(u.encryptedSecret);
    return authenticator.verify({ token, secret, window: 1 });
  }

  disable(userId) {
    this.users.set(userId, { enabled: false, backupHashes: new Set(), attempts: [] });
  }
}

module.exports = { TOTPService };
