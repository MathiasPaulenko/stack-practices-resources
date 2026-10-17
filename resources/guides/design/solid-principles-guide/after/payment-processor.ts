// after/payment-processor.ts
// DIP: the high-level module depends only on abstractions.
// LSP: any PaymentGateway implementation can be substituted.

import type {
  Payment,
  PaymentGateway,
  PaymentRepository,
  PaymentResult,
  PaymentValidator,
  NotificationService,
  Logger,
} from "./interfaces";

export class PaymentProcessor {
  constructor(
    private validator: PaymentValidator,
    private gateway: PaymentGateway,
    private repo: PaymentRepository,
    private notifier: NotificationService,
    private logger: Logger
  ) {}

  async processPayment(payment: Payment): Promise<PaymentResult> {
    this.validator.validate(payment);
    this.logger.log("info", "Processing payment", { amount: payment.amount });

    const result = await this.gateway.charge(payment.amount, payment.currency);

    await this.repo.save(result);
    await this.notifier.notify(
      payment.customerEmail,
      "Payment received",
      `Your payment of ${payment.amount} ${payment.currency} was processed.`
    );
    this.logger.log("info", "Payment completed", { id: result.id });
    return result;
  }
}
