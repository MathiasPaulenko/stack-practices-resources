// before/payment-processor.ts
// Legacy shape: one class validates, charges, logs, emails, and persists.
// Violates SRP (five responsibilities), OCP (adding a gateway means editing
// this method), and DIP (concrete StripeClient / MySQLConnection are created
// inside the class).

interface Payment {
  amount: number;
  currency: string;
  customerEmail: string;
}

interface PaymentResult {
  id: string;
  amount: number;
  currency: string;
}

// --- External SDK stubs (stand-ins for the real SDKs) ---

class StripeClient {
  constructor(private apiKey: string) {}
  charge(amount: number, currency: string): Promise<PaymentResult> {
    return Promise.resolve({ id: "ch_123", amount, currency });
  }
}

class EmailService {
  send(to: string, subject: string, body: string): Promise<void> {
    return Promise.resolve();
  }
}

class MySQLConnection {
  constructor(private host: string, private database: string) {}
  query(sql: string, params: unknown): Promise<void> {
    return Promise.resolve();
  }
}

// --- The violation ---

export class PaymentProcessor {
  async processPayment(payment: Payment): Promise<PaymentResult> {
    // Validates (SRP violation)
    if (!payment.amount || payment.amount <= 0) throw new Error("Invalid");
    // Processes with Stripe (OCP violation - hardcoded)
    const stripe = new StripeClient("sk_live_xxx");
    const result = await stripe.charge(payment.amount, payment.currency);
    // Logs to console (SRP violation)
    console.log("Payment processed:", result);
    // Sends email (SRP violation)
    const email = new EmailService();
    await email.send(payment.customerEmail, "Payment received", "");
    // Saves to MySQL (DIP violation - hardcoded)
    const db = new MySQLConnection("localhost", "payments");
    await db.query("INSERT INTO payments ...", result);
    return result;
  }
}
