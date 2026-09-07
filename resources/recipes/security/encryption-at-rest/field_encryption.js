// Application-level encryption with HKDF key derivation.
// Node 20+, uses built-in crypto module.

const crypto = require('crypto');

class FieldEncryption {
  constructor(masterKey) {
    this.masterKey = Buffer.from(masterKey, 'hex');
  }

  deriveKey(recordId) {
    return crypto.hkdfSync('sha256', this.masterKey, Buffer.from(recordId), 'field-encryption', 32);
  }

  encrypt(plaintext, recordId) {
    const key = Buffer.from(this.deriveKey(recordId));
    const iv = crypto.randomBytes(12);
    const cipher = crypto.createCipheriv('aes-256-gcm', key, iv);

    const ciphertext = Buffer.concat([cipher.update(plaintext, 'utf8'), cipher.final()]);
    const authTag = cipher.getAuthTag();

    return {
      ciphertext: ciphertext.toString('base64'),
      iv: iv.toString('base64'),
      authTag: authTag.toString('base64'),
    };
  }

  decrypt(encrypted, recordId) {
    const key = Buffer.from(this.deriveKey(recordId));
    const iv = Buffer.from(encrypted.iv, 'base64');
    const authTag = Buffer.from(encrypted.authTag, 'base64');
    const ciphertext = Buffer.from(encrypted.ciphertext, 'base64');

    const decipher = crypto.createDecipheriv('aes-256-gcm', key, iv);
    decipher.setAuthTag(authTag);

    return Buffer.concat([decipher.update(ciphertext), decipher.final()]).toString('utf8');
  }
}

module.exports = { FieldEncryption };

// Usage: node field_encryption.js
if (require.main === module) {
  const enc = new FieldEncryption('a'.repeat(64)); // 32-byte hex key
  const pkg = enc.encrypt('hello world', 'record-001');
  console.log(JSON.stringify(pkg, null, 2));
  const plain = enc.decrypt(pkg, 'record-001');
  console.log('Decrypted:', plain);
}
