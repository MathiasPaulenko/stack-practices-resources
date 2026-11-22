// Saga orchestration for distributed transactions (TypeScript).
// Companion to https://stackpractices.com/recipes/microservices-patterns/
// Each step carries its compensating action; on failure, completed steps
// are compensated in reverse order.

export interface SagaStep {
  execute(): Promise<void>;
  compensate(): Promise<void>;
}

export class OrderSaga {
  private steps: SagaStep[] = [];
  private completedSteps: SagaStep[] = [];

  addStep(step: SagaStep) {
    this.steps.push(step);
    return this;
  }

  async execute() {
    for (const step of this.steps) {
      try {
        await step.execute();
        this.completedSteps.push(step);
      } catch (error) {
        // Compensate all completed steps in reverse order
        for (const completed of this.completedSteps.reverse()) {
          await completed.compensate();
        }
        throw new Error(`Saga failed: ${error}`);
      }
    }
  }
}

// Example wiring (inject your real service clients):
//
// const orderSaga = new OrderSaga()
//   .addStep({
//     execute: () => inventoryService.reserve(order.items),
//     compensate: () => inventoryService.release(order.items),
//   })
//   .addStep({
//     execute: () => paymentService.charge(order.total),
//     compensate: () => paymentService.refund(order.total),
//   })
//   .addStep({
//     execute: () => shippingService.createShipment(order),
//     compensate: () => shippingService.cancelShipment(order),
//   });
//
// await orderSaga.execute();
