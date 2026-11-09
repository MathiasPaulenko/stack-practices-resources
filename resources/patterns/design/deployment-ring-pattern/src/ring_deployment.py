"""Deployment Ring Pattern — runnable Python implementation.

Simulates a progressive rollout through rings of increasing size. A mock
health check fails on the third call (ring 2), which forces a rollback of
the rings that already passed.

Run: python ring_deployment.py
"""

from dataclasses import dataclass
from typing import Callable, List, Optional, Dict
from enum import Enum
import time


class RingStatus(Enum):
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    ROLLED_BACK = "rolled_back"
    FAILED = "failed"


@dataclass
class Ring:
    ring_id: int
    name: str
    percentage: float
    status: RingStatus = RingStatus.PENDING
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    health_check_passed: bool = False


@dataclass
class HealthMetrics:
    error_rate: float
    p95_latency_ms: float
    success_rate: float

    def is_healthy(self, max_error_rate: float = 0.05, max_p95: float = 500) -> bool:
        return self.error_rate < max_error_rate and self.p95_latency_ms < max_p95


class RingDeployment:
    def __init__(self, version: str, rings: List[Ring],
                 health_check_fn: Callable[[], HealthMetrics],
                 max_error_rate: float = 0.05, max_p95: float = 500,
                 bake_time_seconds: float = 2.0):
        self.version = version
        self.rings = rings
        self.health_check_fn = health_check_fn
        self.max_error_rate = max_error_rate
        self.max_p95 = max_p95
        self.bake_time = bake_time_seconds
        self.current_ring_idx = 0

    def _deploy_to_ring(self, ring: Ring) -> bool:
        ring.status = RingStatus.ACTIVE
        ring.started_at = time.time()
        print(f"  Deploying v{self.version} to {ring.name} ({ring.percentage}% of users)")

        time.sleep(self.bake_time)

        metrics = self.health_check_fn()
        ring.health_check_passed = metrics.is_healthy(self.max_error_rate, self.max_p95)

        print(f"    Health: error_rate={metrics.error_rate:.2%}, p95={metrics.p95_latency_ms}ms, success={metrics.success_rate:.2%}")

        if ring.health_check_passed:
            ring.status = RingStatus.COMPLETED
            ring.completed_at = time.time()
            print(f"    PASS - Ring {ring.ring_id} completed")
            return True
        else:
            ring.status = RingStatus.FAILED
            print(f"    FAIL - Ring {ring.ring_id} failed health check, rolling back")
            return False

    def execute(self) -> Dict:
        print(f"\n=== Ring Deployment: v{self.version} ===")
        for i, ring in enumerate(self.rings):
            self.current_ring_idx = i
            success = self._deploy_to_ring(ring)
            if not success:
                self._rollback()
                return {"version": self.version, "status": "rolled_back",
                        "failed_ring": ring.ring_id, "rings_completed": i}
        print(f"\nAll rings completed. v{self.version} is live for 100% of users.")
        return {"version": self.version, "status": "completed",
                "rings_completed": len(self.rings)}

    def _rollback(self) -> None:
        for ring in self.rings:
            if ring.status == RingStatus.COMPLETED:
                ring.status = RingStatus.ROLLED_BACK
                print(f"  Rolling back ring {ring.ring_id} ({ring.name})")


if __name__ == "__main__":
    call_count = 0

    def mock_health_check() -> HealthMetrics:
        global call_count
        call_count += 1
        if call_count == 3:
            return HealthMetrics(error_rate=0.08, p95_latency_ms=600, success_rate=0.92)
        return HealthMetrics(error_rate=0.01, p95_latency_ms=120, success_rate=0.99)

    rings = [
        Ring(ring_id=0, name="internal", percentage=1.0),
        Ring(ring_id=1, name="early-adopters", percentage=5.0),
        Ring(ring_id=2, name="canary", percentage=25.0),
        Ring(ring_id=3, name="general", percentage=100.0),
    ]

    deployment = RingDeployment(
        version="2.1.0", rings=rings, health_check_fn=mock_health_check,
        max_error_rate=0.05, max_p95=500, bake_time_seconds=0.5,
    )

    result = deployment.execute()
    print(f"\nResult: {result}")
