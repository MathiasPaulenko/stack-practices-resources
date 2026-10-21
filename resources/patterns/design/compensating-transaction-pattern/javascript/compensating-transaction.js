// Compensating Transaction — runnable saga demo (no dependencies).
// A successful saga and a failing one that triggers reverse-order compensation.
//
// Run: node compensating-transaction.js

class PaymentService {
  constructor() { this.charges = new Map(); }
  charge(orderId, amount) {
    this.charges.set(orderId, { amount, status: "charged" });
    console.log(`  [Payment] Charged $${amount} for ${orderId}`);
    return true;
  }
  refund(orderId) {
    const charge = this.charges.get(orderId);
    if (charge) {
      charge.status = "refunded";
      console.log(`  [Payment] Refunded $${charge.amount} for ${orderId}`);
      return true;
    }
    return false;
  }
}

class InventoryService {
  constructor() {
    this.stock = new Map([["SKU-001", 100]]);
    this.reservations = new Map();
  }
  reserve(orderId, sku, qty) {
    const available = this.stock.get(sku) || 0;
    if (available >= qty) {
      this.stock.set(sku, available - qty);
      this.reservations.set(orderId, { sku, qty });
      console.log(`  [Inventory] Reserved ${qty}x ${sku}`);
      return true;
    }
    console.log(`  [Inventory] Insufficient stock for ${sku}`);
    return false;
  }
  release(orderId) {
    const res = this.reservations.get(orderId);
    if (res) {
      this.stock.set(res.sku, this.stock.get(res.sku) + res.qty);
      console.log(`  [Inventory] Released ${res.qty}x ${res.sku}`);
      this.reservations.delete(orderId);
      return true;
    }
    return false;
  }
}

class SagaOrchestrator {
  constructor() { this.completedSteps = []; }

  async execute(steps) {
    for (const step of steps) {
      console.log(`Executing: ${step.name}`);
      const success = await step.action();
      if (success) {
        this.completedSteps.push(step);
      } else {
        console.log(`${step.name} failed! Compensating...`);
        await this.compensate();
        return { success: false, failedStep: step.name };
      }
    }
    return { success: true };
  }

  async compensate() {
    for (const step of [...this.completedSteps].reverse()) {
      console.log(`Compensating: ${step.name}`);
      try {
        await step.compensate();
      } catch (e) {
        console.error(`WARNING: Compensation failed for ${step.name}: ${e.message}`);
      }
    }
  }
}

async function demo() {
  const payments = new PaymentService();
  const inventory = new InventoryService();
  const saga = new SagaOrchestrator();

  const steps = [
    { name: "charge",
      action: () => payments.charge("ORD-001", 99.99),
      compensate: () => payments.refund("ORD-001") },
    { name: "reserve",
      action: () => inventory.reserve("ORD-001", "SKU-999", 500),  // fails: no stock
      compensate: () => inventory.release("ORD-001") },
  ];

  const result = await saga.execute(steps);
  console.log("Result:", result.success ? "SUCCESS" : "FAILED (compensated)");
}

demo().catch(console.error);
