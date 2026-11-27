import { describe, expect, it } from 'vitest';
import { Order } from '../src/domain/order';
import { OrderValidator } from '../src/domain/order-validator';
import { OrderRepository } from '../src/infra/order-repository';
import { OrderNotifier } from '../src/infra/order-notifier';
import { OrderService } from '../src/order-service';
import { NoDiscount, PercentageDiscount } from '../src/discount/discount-strategy';
import type { Writable } from '../src/infra/interfaces';
import type { Order as OrderType } from '../src/domain/order';

class MockRepo implements Writable {
  saved: OrderType[] = [];
  async write(order: OrderType): Promise<void> {
    this.saved.push(order);
  }
}

const order = () =>
  new Order('o-1', [{ sku: 'SKU-1', quantity: 1, priceCents: 10000 }], 10000);

describe('OrderService', () => {
  it('saves a valid order', async () => {
    const repo = new MockRepo();
    const svc = new OrderService(repo, new OrderValidator(), new OrderNotifier(), new NoDiscount());
    await svc.createOrder(order());
    expect(repo.saved).toHaveLength(1);
  });

  it('applies the injected discount strategy', async () => {
    const repo = new MockRepo();
    const svc = new OrderService(repo, new OrderValidator(), new OrderNotifier(), new PercentageDiscount(10));
    await svc.createOrder(order());
    expect(repo.saved[0].total).toBe(9000);
  });

  it('rejects an order without items', async () => {
    const svc = new OrderService(new OrderRepository(), new OrderValidator(), new OrderNotifier(), new NoDiscount());
    await expect(svc.createOrder(new Order('o-2', [], 0))).rejects.toThrow('must have items');
  });
});
