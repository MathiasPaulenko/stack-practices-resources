// aes-gcm.ts — AES-256-GCM encryption and decryption
// Companion to https://stackpractices.com/guides/complete-guide-encryption-at-rest/
import crypto from 'crypto';

const ALGORITHM = 'aes-256-gcm';
const IV_LENGTH = 12; // 96-bit IV for GCM (recommended)
const TAG_LENGTH = 16; // 128-bit auth tag

export interface EncryptedData {
  ciphertext: string; // base64
  iv: string; // base64
  tag: string; // base64
  keyVersion: number; // for key rotation
}

export function encrypt(
  plaintext: string,
  key: Buffer,
  keyVersion: number = 1,
): EncryptedData {
  const iv = crypto.randomBytes(IV_LENGTH);
  const cipher = crypto.createCipheriv(ALGORITHM, key, iv);

  const ciphertext = Buffer.concat([
    cipher.update(plaintext, 'utf8'),
    cipher.final(),
  ]);

  const tag = cipher.getAuthTag();

  return {
    ciphertext: ciphertext.toString('base64'),
    iv: iv.toString('base64'),
    tag: tag.toString('base64'),
    keyVersion,
  };
}

export function decrypt(data: EncryptedData, key: Buffer): string {
  const decipher = crypto.createDecipheriv(
    ALGORITHM,
    key,
    Buffer.from(data.iv, 'base64'),
  );

  decipher.setAuthTag(Buffer.from(data.tag, 'base64'));

  const plaintext = Buffer.concat([
    decipher.update(Buffer.from(data.ciphertext, 'base64')),
    decipher.final(),
  ]);

  return plaintext.toString('utf8');
}
