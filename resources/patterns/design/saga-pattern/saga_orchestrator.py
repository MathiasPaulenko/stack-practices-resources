"""Orchestrated saga: travel booking with compensating transactions.

The `charge_payment` step always fails so you can watch the rollback path:
completed steps are undone in reverse order through their compensations.

Run: python saga_orchestrator.py   (no dependencies)
"""

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional


@dataclass
class SagaResult:
    success: bool
    data: Any = None
    error: Optional[str] = None
    step_index: int = 0


class SagaStep:
    def __init__(self, name: str, action: Callable, compensation: Callable = None):
        self.name = name
        self.action = action
        self.compensation = compensation


class SagaOrchestrator:
    def __init__(self):
        self.steps: List[SagaStep] = []
        self.completed: List[Dict] = []

    def add_step(self, name: str, action: Callable, compensation: Callable = None):
        self.steps.append(SagaStep(name, action, compensation))

    def execute(self, context: Dict) -> SagaResult:
        self.completed = []
        for i, step in enumerate(self.steps):
            try:
                step.action(context)
                self.completed.append({"step": step.name, "context": dict(context)})
                print(f"Step '{step.name}' completed")
            except Exception as e:
                print(f"Step '{step.name}' failed: {e}")
                self.rollback(i)
                return SagaResult(success=False, error=str(e), step_index=i)
        return SagaResult(success=True, data=context)

    def rollback(self, failed_index: int):
        print(f"Rolling back {failed_index} completed steps...")
        for j in range(failed_index - 1, -1, -1):
            step = self.steps[j]
            if step.compensation:
                try:
                    state = self.completed[j]
                    step.compensation(state["context"])
                    print(f"Compensated '{step.name}'")
                except Exception as e:
                    print(f"Compensation failed for '{step.name}': {e}")


if __name__ == "__main__":
    saga = SagaOrchestrator()

    saga.add_step(
        "reserve_flight",
        action=lambda ctx: ctx.update({"flight": "FL123"}) or True,
        compensation=lambda ctx: print("Canceling flight reservation"),
    )
    saga.add_step(
        "reserve_hotel",
        action=lambda ctx: ctx.update({"hotel": "HT456"}) or True,
        compensation=lambda ctx: print("Canceling hotel reservation"),
    )
    saga.add_step(
        "charge_payment",
        action=lambda ctx: (_ for _ in ()).throw(Exception("Payment declined")),
        compensation=lambda ctx: print("Refunding payment"),
    )

    result = saga.execute({"user": "alice"})
    print(f"Saga success: {result.success}")
