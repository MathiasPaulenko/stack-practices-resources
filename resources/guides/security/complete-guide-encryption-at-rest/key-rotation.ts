// key-rotation.ts — Rotate data encryption keys in batches
// Companion to https://stackpractices.com/guides/complete-guide-encryption-at-rest/
import { KmsClient } from './kms-client';
import { Database } from './encrypted-field';

// Batch re-encryption: find records on the old key version, decrypt,
// re-encrypt with the new version, update in place. Run during
// low-traffic windows and keep both key versions live until done.
export class KeyRotationService {
  constructor(
    private readonly kms: KmsClient,
    private readonly db: Database,
  ) {}

  async rotateKeys(): Promise<void> {
    // 1. Find all records with old key version
    const records = await this.db.query(
      `SELECT id, encrypted_data FROM sensitive_data WHERE key_version = $1`,
      [1], // old key version
    );

    for (const record of records.rows) {
      // 2. Decrypt with old key
      const plaintext = await this.decrypt(record.encrypted_data, 1);

      // 3. Re-encrypt with new key
      const reencrypted = await this.encrypt(plaintext, 2); // new key version

      // 4. Update record
      await this.db.query(
        `UPDATE sensitive_data SET encrypted_data = $1, key_version = $2 WHERE id = $3`,
        [reencrypted, 2, record.id],
      );
    }

    console.log(`Rotated ${records.rows.length} records to key version 2`);
  }

  private async encrypt(_plaintext: string, _version: number): Promise<string> {
    // Wire to your envelope encryption + chosen DEK version.
    throw new Error('Not implemented — see the guide for wiring.');
  }

  private async decrypt(_data: string, _version: number): Promise<string> {
    throw new Error('Not implemented — see the guide for wiring.');
  }
}
