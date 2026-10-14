// encrypted-field.ts — Transparent field encryption in the data layer
// Companion to https://stackpractices.com/guides/complete-guide-encryption-at-rest/
import { EnvelopeEncryption, EnvelopeEncryptedData } from './envelope-encryption';

// Minimal DB interface — adapt to pg, knex, Prisma, or your driver of choice.
export interface Database {
  query(sql: string, params: unknown[]): Promise<{ rows: any[] }>;
}

export class EncryptedField {
  constructor(private readonly envelopeEncryption: EnvelopeEncryption) {}

  async encryptField(value: string): Promise<string> {
    const encrypted = await this.envelopeEncryption.encrypt(value);
    return JSON.stringify(encrypted);
  }

  async decryptField(storedValue: string): Promise<string> {
    const data = JSON.parse(storedValue) as EnvelopeEncryptedData;
    return this.envelopeEncryption.decrypt(data);
  }
}

export interface CreateUserInput {
  email: string;
  ssn: string;
  phone: string;
}

export interface User {
  id: string;
  email: string;
  ssn: string;
  phone: string;
}

// Repository with transparent encryption: sensitive fields are encrypted
// before they reach SQL and decrypted on the way out.
export class UserRepository {
  constructor(
    private readonly db: Database,
    private readonly encryptedField: EncryptedField,
  ) {}

  async createUser(data: CreateUserInput): Promise<User> {
    const encryptedSsn = await this.encryptedField.encryptField(data.ssn);
    const encryptedPhone = await this.encryptedField.encryptField(data.phone);

    const result = await this.db.query(
      `INSERT INTO users (email, encrypted_ssn, encrypted_phone, encryption_metadata)
       VALUES ($1, $2, $3, $4) RETURNING id, email`,
      [data.email, encryptedSsn, encryptedPhone, null],
    );

    return result.rows[0];
  }

  async getUser(id: string): Promise<User | null> {
    const result = await this.db.query(
      `SELECT * FROM users WHERE id = $1`,
      [id],
    );

    const row = result.rows[0];
    if (!row) return null;

    return {
      id: row.id,
      email: row.email,
      ssn: await this.encryptedField.decryptField(row.encrypted_ssn),
      phone: await this.encryptedField.decryptField(row.encrypted_phone),
    };
  }
}
