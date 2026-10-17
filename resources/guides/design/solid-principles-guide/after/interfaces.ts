// after/interfaces.ts
// The contracts the payment flow depends on (ISP: each interface is narrow).

export interface Payment {
  amount: number;
  currency: string;
  customerEmail: string;
}

export interface PaymentResult {
  id: string;
  amount: number;
  currency: string;
}

export interface PaymentValidator {
  validate(payment: Payment): void;
}

export interface PaymentGateway {
  charge(amount: number, currency: string): Promise<PaymentResult>;
}

export interface PaymentRepository {
  save(result: PaymentResult): Promise<void>;
}

export interface NotificationService {
  notify(email: string, subject: string, body: string): Promise<void>;
}

export interface Logger {
  log(level: string, message: string, meta?: object): void;
}
