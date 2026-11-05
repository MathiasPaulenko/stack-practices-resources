// service.ts — Child loggers with bound context
import { logger } from "./logger";

interface OrderItem {
  price: number;
  quantity: number;
}

class OrderService {
  private logger = logger.child({ service: "order-service" });
  private paymentService!: { charge(u: string, t: number): Promise<{ id: string; amount: number }> };
  private orderRepo!: { create(o: unknown): Promise<{ id: string }> };

  async createOrder(userId: string, items: OrderItem[]) {
    this.logger.info({ userId, itemCount: items.length }, "order_creation_started");

    const total = items.reduce((sum, item) => sum + item.price * item.quantity, 0);

    try {
      const payment = await this.paymentService.charge(userId, total);
      this.logger.info({ paymentId: payment.id, amount: payment.amount }, "payment_processed");

      const order = await this.orderRepo.create({ userId, items, paymentId: payment.id });
      this.logger.info({ orderId: order.id, userId, total }, "order_created");
      return order;
    } catch (error) {
      this.logger.error({ err: error, userId, total }, "order_creation_failed");
      throw error;
    }
  }
}
