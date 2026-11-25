// Saga orchestrator with compensating transactions + Temporal state-machine variant
// From https://stackpractices.com/recipes/saga-pattern-recipe/

class OrderSagaOrchestrator {
  constructor(
    private orderService: OrderService,
    private inventoryService: InventoryService,
    private paymentService: PaymentService,
    private shippingService: ShippingService
  ) {}

  async execute(orderData: OrderData): Promise<SagaResult> {
    const state: SagaState = { orderId: generateUUID(), status: 'started' };

    try {
      // Step 1: Create order
      await this.orderService.createOrder({ ...orderData, id: state.orderId });
      state.orderCreated = true;

      // Step 2: Reserve inventory
      await this.inventoryService.reserve(state.orderId, orderData.items);
      state.inventoryReserved = true;

      // Step 3: Process payment
      await this.paymentService.charge(state.orderId, orderData.total);
      state.paymentProcessed = true;

      // Step 4: Ship order
      await this.shippingService.schedule(state.orderId, orderData.address);
      state.shipped = true;

      return { success: true, orderId: state.orderId };
    } catch (error) {
      await this.compensate(state);
      return { success: false, orderId: state.orderId, error: error.message };
    }
  }

  private async compensate(state: SagaState): Promise<void> {
    if (state.shipped) {
      await this.shippingService.cancel(state.orderId);
    }
    if (state.paymentProcessed) {
      await this.paymentService.refund(state.orderId);
    }
    if (state.inventoryReserved) {
      await this.inventoryService.release(state.orderId);
    }
    if (state.orderCreated) {
      await this.orderService.cancelOrder(state.orderId);
    }
  }
}


// --- Temporal / Cadence state-machine variant ---

import { workflow, activity } from '@temporalio/workflow';

const createOrder = activity('createOrder');
const reserveInventory = activity('reserveInventory');
const processPayment = activity('processPayment');
const scheduleShipping = activity('scheduleShipping');
const refundPayment = activity('refundPayment');
const releaseInventory = activity('releaseInventory');

async function orderSaga(orderData: OrderData): Promise<void> {
  const orderId = await createOrder(orderData);

  try {
    await reserveInventory({ orderId, items: orderData.items });
  } catch (error) {
    await compensateOrder(orderId);
    throw error;
  }

  try {
    await processPayment({ orderId, amount: orderData.total });
  } catch (error) {
    await releaseInventory({ orderId });
    await compensateOrder(orderId);
    throw error;
  }

  try {
    await scheduleShipping({ orderId, address: orderData.address });
  } catch (error) {
    await refundPayment({ orderId });
    await releaseInventory({ orderId });
    await compensateOrder(orderId);
    throw error;
  }
}
