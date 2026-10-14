// kms-client.ts — Abstract KMS interface + AWS KMS implementation
// Companion to https://stackpractices.com/guides/complete-guide-encryption-at-rest/
//
// Requires: npm install @aws-sdk/client-kms
// Env: AWS_REGION (or edit below), KMS_KEY_ID
import { KMSClient, EncryptCommand, DecryptCommand } from '@aws-sdk/client-kms';

export interface KmsClient {
  encrypt(dataKey: Buffer): Promise<{ ciphertext: string; keyVersion: number }>;
  decrypt(ciphertext: string, keyVersion: number): Promise<Buffer>;
  rotateKey(): Promise<void>;
}

export class AwsKmsClient implements KmsClient {
  private client = new KMSClient({ region: 'us-east-1' });
  private keyId = process.env.KMS_KEY_ID!;

  async encrypt(
    dataKey: Buffer,
  ): Promise<{ ciphertext: string; keyVersion: number }> {
    const command = new EncryptCommand({
      KeyId: this.keyId,
      Plaintext: dataKey,
    });
    const response = await this.client.send(command);
    return {
      ciphertext: Buffer.from(response.CiphertextBlob!).toString('base64'),
      keyVersion: 1, // KMS tracks version internally
    };
  }

  async decrypt(ciphertext: string, _keyVersion: number): Promise<Buffer> {
    const command = new DecryptCommand({
      CiphertextBlob: Buffer.from(ciphertext, 'base64'),
    });
    const response = await this.client.send(command);
    return Buffer.from(response.Plaintext!);
  }

  async rotateKey(): Promise<void> {
    // AWS KMS auto-rotates keys annually when enabled.
    // Manual rotation creates a new key version.
  }
}
