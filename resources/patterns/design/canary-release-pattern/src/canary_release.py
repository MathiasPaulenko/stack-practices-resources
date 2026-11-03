from dataclasses import dataclass, field
from typing import Callable, List, Optional, Dict
from enum import Enum
import time

class CanaryStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    PROMOTED = "promoted"
    ROLLED_BACK = "rolled_back"

@dataclass
class HealthMetrics:
    error_rate: float
    p95_latency_ms: float
    success_rate: float

    def is_healthy(self, max_error_rate: float = 0.02, max_p95: float = 300) -> bool:
        return self.error_rate <= max_error_rate and self.p95_latency_ms <= max_p95

@dataclass
class CanaryStage:
    percentage: float
    bake_time_seconds: float
    metrics: Optional[HealthMetrics] = None
    passed: bool = False

class CanaryRelease:
    def __init__(self, version: str, stable_version: str,
                 health_check_fn: Callable[[], HealthMetrics],
                 stages: Optional[List[CanaryStage]] = None,
                 max_error_rate: float = 0.02, max_p95: float = 300):
        self.version = version
        self.stable_version = stable_version
        self.health_check_fn = health_check_fn
        self.max_error_rate = max_error_rate
        self.max_p95 = max_p95
        self.status = CanaryStatus.PENDING
        self.current_stage_idx = -1
        # Demo bake times; real stages run for minutes, not fractions of a second.
        self.stages = stages or [
            CanaryStage(percentage=1.0, bake_time_seconds=0.1),
            CanaryStage(percentage=5.0, bake_time_seconds=0.1),
            CanaryStage(percentage=25.0, bake_time_seconds=0.1),
            CanaryStage(percentage=50.0, bake_time_seconds=0.1),
            CanaryStage(percentage=100.0, bake_time_seconds=0.1),
        ]

    def _run_stage(self, stage: CanaryStage) -> bool:
        self.current_stage_idx += 1
        self.status = CanaryStatus.RUNNING
        print(f"  Canary at {stage.percentage}% -> stable={100 - stage.percentage}%")

        time.sleep(stage.bake_time_seconds)
        metrics = self.health_check_fn()
        stage.metrics = metrics
        stage.passed = metrics.is_healthy(self.max_error_rate, self.max_p95)

        print(f"    error_rate={metrics.error_rate:.2%}, p95={metrics.p95_latency_ms}ms, success={metrics.success_rate:.2%}")

        if stage.passed:
            print(f"    PASS - advancing to next stage")
            return True
        else:
            print(f"    FAIL - rolling back canary")
            self.status = CanaryStatus.ROLLED_BACK
            return False

    def execute(self) -> Dict:
        print(f"\n=== Canary Release: v{self.version} (stable: v{self.stable_version}) ===")
        for i, stage in enumerate(self.stages):
            if not self._run_stage(stage):
                return self._result(rolled_back=True, failed_stage=i)
        self.status = CanaryStatus.PROMOTED
        print(f"\nCanary promoted. v{self.version} is now at 100%.")
        return self._result(rolled_back=False, failed_stage=None)

    def _result(self, rolled_back: bool, failed_stage: Optional[int]) -> Dict:
        return {
            "version": self.version,
            "status": self.status.value,
            "rolled_back": rolled_back,
            "stages_passed": self.current_stage_idx if rolled_back else len(self.stages),
            "failed_stage": failed_stage,
            "max_percentage_reached": self.stages[self.current_stage_idx].percentage if rolled_back else 100.0,
        }

# Usage
call_count = 0
def mock_health_check() -> HealthMetrics:
    global call_count
    call_count += 1
    if call_count == 3:
        return HealthMetrics(error_rate=0.05, p95_latency_ms=400, success_rate=0.95)
    return HealthMetrics(error_rate=0.005, p95_latency_ms=80, success_rate=0.995)

canary = CanaryRelease(
    version="3.0.0", stable_version="2.9.0",
    health_check_fn=mock_health_check,
    max_error_rate=0.02, max_p95=300,
)

result = canary.execute()
print(f"\nResult: {result}")
