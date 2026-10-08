// Temporal workflow — order processing (TypeScript SDK)
// Requires: npm install @temporalio/workflow @temporalio/activity

import { proxyActivities } from '@temporalio/workflow';
import type * as activities from './activities';

export interface OrderInput {
  id: string;
  items: { sku: string; qty: number }[];
  total: number;
  address: string;
}

export interface OrderResult {
  status: 'completed' | 'failed';
  orderId: string;
}

const {
  validateOrder,
  checkInventory,
  processPayment,
  sendEmail,
  updateAnalytics,
  scheduleShipment,
  releaseInventory,
} = proxyActivities<typeof activities>({
  startToCloseTimeout: '30 seconds',
  retry: { maximumAttempts: 3, backoffCoefficient: 2 },
});

export async function orderWorkflow(order: OrderInput): Promise<OrderResult> {
  try {
    await validateOrder(order);
    await checkInventory(order.items);
    await processPayment({ orderId: order.id, amount: order.total });

    // Parallel execution — fan-out
    await Promise.all([
      sendEmail({ orderId: order.id, template: 'confirmation' }),
      updateAnalytics({ event: 'order_placed', orderId: order.id }),
    ]);

    await scheduleShipment({ orderId: order.id, address: order.address });

    return { status: 'completed', orderId: order.id };
  } catch (error) {
    if ((error as Error & { type?: string }).type === 'PaymentFailed') {
      await releaseInventory({ orderId: order.id });
    }
    throw error;
  }
}
