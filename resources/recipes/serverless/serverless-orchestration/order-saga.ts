// Temporal saga with compensation — each step registers its rollback
// before advancing. On failure, compensations run in reverse order.

import { proxyActivities } from '@temporalio/workflow';
import type * as activities from './activities';
import type { OrderInput } from './order-workflow';

const Activities = proxyActivities<typeof activities>({
  startToCloseTimeout: '30 seconds',
});

export async function orderSaga(order: OrderInput): Promise<void> {
  const compensations: (() => Promise<void>)[] = [];

  try {
    await Activities.reserveInventory(order);
    compensations.push(() => Activities.releaseInventory({ orderId: order.id }));

    await Activities.chargePayment({ orderId: order.id, amount: order.total });
    compensations.push(() => Activities.refundPayment({ orderId: order.id }));

    await Activities.scheduleShipment({ orderId: order.id, address: order.address });
    // No compensation for shipment — once shipped, it's done
  } catch (err) {
    // Run compensations in reverse order
    for (const compensate of compensations.reverse()) {
      try {
        await compensate();
      } catch (c) {
        console.error('Compensation failed:', c);
      }
    }
    throw err;
  }
}
