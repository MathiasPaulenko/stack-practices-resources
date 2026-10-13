// Orchestrated saga: travel booking with compensating transactions.
// The `chargePayment` step always fails so you can watch the rollback path.
// Run: node sagaOrchestrator.mjs   (no dependencies)

class SagaStep {
  constructor(name, action, compensation) {
    this.name = name;
    this.action = action;
    this.compensation = compensation;
  }
}

class SagaOrchestrator {
  constructor() {
    this.steps = [];
    this.completed = [];
  }

  addStep(name, action, compensation) {
    this.steps.push(new SagaStep(name, action, compensation));
  }

  async execute(context) {
    this.completed = [];
    for (let i = 0; i < this.steps.length; i++) {
      try {
        await this.steps[i].action(context);
        this.completed.push({ step: this.steps[i].name, context: { ...context } });
        console.log(`Step '${this.steps[i].name}' completed`);
      } catch (e) {
        console.log(`Step '${this.steps[i].name}' failed: ${e.message}`);
        await this.rollback(i);
        return { success: false, error: e.message, stepIndex: i };
      }
    }
    return { success: true, data: context };
  }

  async rollback(failedIndex) {
    console.log(`Rolling back ${failedIndex} completed steps...`);
    for (let j = failedIndex - 1; j >= 0; j--) {
      const step = this.steps[j];
      if (step.compensation) {
        try {
          await step.compensation(this.completed[j].context);
          console.log(`Compensated '${step.name}'`);
        } catch (e) {
          console.log(`Compensation failed for '${step.name}': ${e.message}`);
        }
      }
    }
  }
}

const saga = new SagaOrchestrator();
saga.addStep("reserveFlight",
  async (ctx) => { ctx.flight = "FL123"; },
  async () => console.log("Canceling flight")
);
saga.addStep("reserveHotel",
  async (ctx) => { ctx.hotel = "HT456"; },
  async () => console.log("Canceling hotel")
);
saga.addStep("chargePayment",
  async () => { throw new Error("Payment declined"); },
  async () => console.log("Refunding payment")
);

saga.execute({ user: "alice" }).then(r => console.log("Success:", r.success));
