// Driven adapters: concrete implementations of the secondary ports.
// Swap them per environment (Postgres in production, in-memory in tests)
// without touching the domain.

import type { Pool } from "pg";
import type { EmailService, UserRepository } from "./ports";
import { User } from "./user-registration-service";

export class PostgresUserRepository implements UserRepository {
  constructor(private db: Pool) {}

  async findById(id: string): Promise<User | null> {
    const result = await this.db.query("SELECT * FROM users WHERE id = $1", [id]);
    return result.rows.length ? this.toUser(result.rows[0]) : null;
  }

  async findByEmail(email: string): Promise<User | null> {
    const result = await this.db.query("SELECT * FROM users WHERE email = $1", [email]);
    return result.rows.length ? this.toUser(result.rows[0]) : null;
  }

  async save(user: User): Promise<void> {
    await this.db.query(
      `INSERT INTO users (id, email, name, is_verified)
       VALUES ($1, $2, $3, $4)
       ON CONFLICT (id) DO UPDATE SET email = $2, name = $3, is_verified = $4`,
      [user.id, user.email, user.name, user.isVerified]
    );
  }

  private toUser(row: {
    id: string;
    email: string;
    name: string;
    is_verified: boolean;
  }): User {
    return new User(row.id, row.email, row.name, row.is_verified);
  }
}

export class InMemoryUserRepository implements UserRepository {
  private users: Map<string, User> = new Map();

  async findById(id: string): Promise<User | null> {
    return this.users.get(id) ?? null;
  }

  async findByEmail(email: string): Promise<User | null> {
    return [...this.users.values()].find((u) => u.email === email) ?? null;
  }

  async save(user: User): Promise<void> {
    this.users.set(user.id, user);
  }
}

export class SmtpEmailService implements EmailService {
  async send(user: User, subject: string, body: string): Promise<void> {
    // Wire your SMTP transport here (nodemailer, SES, SendGrid, etc.)
    void user;
    void subject;
    void body;
  }
}

export class MockEmailService implements EmailService {
  sentEmails: Array<{ user: User; subject: string; body: string }> = [];

  async send(user: User, subject: string, body: string): Promise<void> {
    this.sentEmails.push({ user, subject, body });
  }
}
