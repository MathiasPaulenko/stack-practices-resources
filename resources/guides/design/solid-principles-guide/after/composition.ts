// after/composition.ts
// Composition root: the single place where abstractions meet implementations.

import { PaymentProcessor } from "./payment-processor";
import {
  EmailNotificationService,
  PayPalClient,
  PayPalGateway,
  PaymentValidatorImpl,
  PostgresPaymentRepository,
  StripeClient,
  StripeGateway,
  WinstonLogger,
} from "./implementations";
import type { PaymentResult } from "./interfaces";

const stripeClient = new StripeClient("sk_live_xxx");
const paypalClient = new PayPalClient();
const db = { query: async (_sql: string, _params: unknown) => {} };
const smtp = { send: async (_to: string, _s: string, _b: string) => {} };

// LSP: any PaymentGateway implementation works
export const processor = new PaymentProcessor(
  new PaymentValidatorImpl(),
  new StripeGateway(stripeClient), // or new PayPalGateway(paypalClient)
  new PostgresPaymentRepository(db),
  new EmailNotificationService(smtp),
  new WinstonLogger()
);

// Testing: mock everything via the interfaces — no patching framework needed
const mockValidator = { validate: () => {} };
const mockGateway = {
  charge: (amount: number, currency: string): Promise<PaymentResult> =>
    Promise.resolve({ id: "mock", amount, currency }),
};
const mockRepo = { save: async () => {} };
const mockNotifier = { notify: async () => {} };
const mockLogger = { log: () => {} };

export const testProcessor = new PaymentProcessor(
  mockValidator,
  mockGateway,
  mockRepo,
  mockNotifier,
  mockLogger
);
