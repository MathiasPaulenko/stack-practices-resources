// envelope-encryption.ts — Envelope encryption pattern
// Companion to https://stackpractices.com/guides/complete-guide-encryption-at-rest/
import crypto from 'crypto';
import { encrypt, decrypt, EncryptedData } from './aes-gcm';
import { KmsClient } from './kms-client';

export interface EnvelopeEncryptedData extends EncryptedData {
  encryptedDek: string; // base64 DEK wrapped by the KMS KEK
  dekKeyVersion: number;
}

export class EnvelopeEncryption {
  constructor(private readonly kms: KmsClient) {}

  async encrypt(plaintext: string): Promise<EnvelopeEncryptedData> {
    // 1. Generate a data encryption key (DEK)
    const dek = crypto.randomBytes(32); // 256-bit DEK

    // 2. Encrypt the data with the DEK
    const encrypted = encrypt(plaintext, dek);

    // 3. Encrypt the DEK with the KMS (KEK)
    const encryptedDek = await this.kms.encrypt(dek);

    // 4. Zero out the DEK from memory
    dek.fill(0);

    return {
      ...encrypted,
      encryptedDek: encryptedDek.ciphertext,
      dekKeyVersion: encryptedDek.keyVersion,
    };
  }

  async decrypt(data: EnvelopeEncryptedData): Promise<string> {
    // 1. Decrypt the DEK using KMS
    const dek = await this.kms.decrypt(data.encryptedDek, data.dekKeyVersion);

    // 2. Decrypt the data with the DEK
    const plaintext = decrypt(
      {
        ciphertext: data.ciphertext,
        iv: data.iv,
        tag: data.tag,
        keyVersion: data.keyVersion,
      },
      dek,
    );

    // 3. Zero out the DEK
    dek.fill(0);

    return plaintext;
  }
}
