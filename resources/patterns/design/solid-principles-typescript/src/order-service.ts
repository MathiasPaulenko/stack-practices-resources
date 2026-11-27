import type { Order } from './domain/order';
import type { OrderValidator } from './domain/order-validator';
import type { OrderNotifier } from './infra/order-notifier';
import type { DiscountStrategy } from './discount/discount-strategy';
import type { Writable } from './infra/interfaces';

// DIP: the service knows interfaces, never concrete implementations.
export class OrderService {
  constructor(
    private repo: Writable,
    private validator: OrderValidator,
    private notifier: OrderNotifier,
    private discount: DiscountStrategy
  ) {}

  async createOrder(order: Order): Promise<void> {
    const errors = this.validator.validate(order);
    if (errors.length > 0) throw new Error(errors.join(', '));
    order.total = this.discount.apply(order);
    await this.repo.write(order);
    await this.notifier.notify(order);
  }
}
