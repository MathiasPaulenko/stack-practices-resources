import type { Order } from '../domain/order';

export class OrderNotifier {
  async notify(order: Order): Promise<void> {
    // In production: call the email service. The seam is this class —
    // OrderService never touches SMTP.
  }
}
