// after/implementations.ts
// Concrete implementations. Each class has one responsibility (SRP) and new
// gateways are added here without touching PaymentProcessor (OCP).

import type {
  Payment,
  PaymentGateway,
  PaymentRepository,
  PaymentResult,
  PaymentValidator,
  NotificationService,
  Logger,
} from "./interfaces";

// --- External SDK stubs (stand-ins for the real SDKs) ---

export class StripeClient {
  constructor(private apiKey: string) {}
  charge(amount: number, currency: string): Promise<PaymentResult> {
    return Promise.resolve({ id: "ch_123", amount, currency });
  }
}

export class PayPalClient {
  createOrder(amount: number, currency: string): Promise<PaymentResult> {
    return Promise.resolve({ id: "pp_456", amount, currency });
  }
}

// --- SRP: one class, one responsibility ---

export class PaymentValidatorImpl implements PaymentValidator {
  validate(payment: Payment): void {
    if (!payment.amount || payment.amount <= 0)
      throw new Error("Invalid amount");
    if (!payment.currency || payment.currency.length !== 3)
      throw new Error("Invalid currency");
  }
}

// --- OCP: new gateways extend without modifying existing code ---

export class StripeGateway implements PaymentGateway {
  constructor(private client: StripeClient) {}
  charge(amount: number, currency: string): Promise<PaymentResult> {
    return this.client.charge(amount, currency);
  }
}

export class PayPalGateway implements PaymentGateway {
  constructor(private client: PayPalClient) {}
  charge(amount: number, currency: string): Promise<PaymentResult> {
    return this.client.createOrder(amount, currency);
  }
}

export class PostgresPaymentRepository implements PaymentRepository {
  constructor(private db: { query(sql: string, params: unknown): Promise<void> }) {}
  async save(result: PaymentResult): Promise<void> {
    await this.db.query("INSERT INTO payments (id, amount, currency) VALUES (...)", result);
  }
}

export class EmailNotificationService implements NotificationService {
  constructor(private smtp: { send(to: string, subject: string, body: string): Promise<void> }) {}
  notify(email: string, subject: string, body: string): Promise<void> {
    return this.smtp.send(email, subject, body);
  }
}

export class WinstonLogger implements Logger {
  log(level: string, message: string, meta?: object): void {
    console.log(`[${level}] ${message}`, meta ?? "");
  }
}
