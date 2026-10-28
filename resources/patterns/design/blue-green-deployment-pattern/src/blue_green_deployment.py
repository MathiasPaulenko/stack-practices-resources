from dataclasses import dataclass
from typing import Callable, List, Dict
from enum import Enum
import time

class EnvironmentColor(Enum):
    BLUE = "blue"
    GREEN = "green"

class EnvironmentStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    DEPLOYING = "deploying"
    TESTING = "testing"

@dataclass
class Environment:
    color: EnvironmentColor
    version: str = ""
    status: EnvironmentStatus = EnvironmentStatus.INACTIVE
    health: bool = False
    instance_count: int = 0

@dataclass
class DeploymentResult:
    success: bool
    active_environment: EnvironmentColor
    version: str
    rollback_performed: bool = False
    message: str = ""

class BlueGreenDeployment:
    def __init__(self):
        self.blue = Environment(color=EnvironmentColor.BLUE, version="1.0.0",
                                status=EnvironmentStatus.ACTIVE, health=True, instance_count=3)
        self.green = Environment(color=EnvironmentColor.GREEN, version="",
                                 status=EnvironmentStatus.INACTIVE, health=False, instance_count=0)
        self._active: Environment = self.blue
        self._inactive: Environment = self.green
        self._history: List[Dict] = []

    @property
    def active(self) -> Environment:
        return self._active

    @property
    def inactive(self) -> Environment:
        return self._inactive

    def _switch(self) -> None:
        self._active, self._inactive = self._inactive, self._active
        self._active.status = EnvironmentStatus.ACTIVE
        self._inactive.status = EnvironmentStatus.INACTIVE

    def deploy(self, new_version: str, smoke_tests: List[Callable] = None) -> DeploymentResult:
        print(f"\n=== Blue-Green Deploy: v{new_version} ===")
        smoke_tests = smoke_tests or []

        target = self.inactive
        print(f"  Deploying to {target.color.value} (currently inactive)")

        target.status = EnvironmentStatus.DEPLOYING
        target.version = new_version
        target.instance_count = 3
        time.sleep(0.2)
        print(f"  Deployed v{new_version} to {target.color.value}")

        target.status = EnvironmentStatus.TESTING
        all_passed = True
        for test in smoke_tests:
            result = test()
            if not result:
                all_passed = False
                break

        if not all_passed:
            target.health = False
            target.status = EnvironmentStatus.INACTIVE
            print(f"  Smoke tests FAILED on {target.color.value}, keeping {self.active.color.value} active")
            return DeploymentResult(success=False, active_environment=self.active.color,
                                    version=self.active.version, message="Smoke tests failed")

        target.health = True
        print(f"  Smoke tests passed on {target.color.value}")

        old_active = self.active
        self._switch()
        print(f"  Switched traffic: {self.active.color.value} (v{self.active.version}) is now active")
        print(f"  {old_active.color.value} (v{old_active.version}) is now inactive")

        self._history.append({"version": new_version, "active": self.active.color.value,
                              "timestamp": time.time()})
        return DeploymentResult(success=True, active_environment=self.active.color,
                                version=new_version, message="Deployment successful")

    def rollback(self) -> DeploymentResult:
        print(f"\n=== Rollback ===")
        if self.inactive.health and self.inactive.version:
            old_active = self.active
            self._switch()
            print(f"  Rolled back to {self.active.color.value} (v{self.active.version})")
            return DeploymentResult(success=True, active_environment=self.active.color,
                                    version=self.active.version, rollback_performed=True,
                                    message="Rollback successful")
        return DeploymentResult(success=False, active_environment=self.active.color,
                                version=self.active.version, message="No healthy environment to roll back to")

    def status(self) -> Dict:
        return {
            "active": {"color": self.active.color.value, "version": self.active.version,
                       "instances": self.active.instance_count},
            "inactive": {"color": self.inactive.color.value, "version": self.inactive.version,
                         "instances": self.inactive.instance_count, "health": self.inactive.health},
            "history": self._history,
        }

# Usage
bg = BlueGreenDeployment()
print(f"Initial state: {bg.status()}")

def test_api_response() -> bool:
    print("    Running test: API response")
    return True

def test_db_connection() -> bool:
    print("    Running test: DB connection")
    return True

result = bg.deploy("2.0.0", smoke_tests=[test_api_response, test_db_connection])
print(f"Result: {result}")
print(f"State: {bg.status()}")

print("\n=== Simulating issue, rolling back ===")
rollback = bg.rollback()
print(f"Rollback: {rollback}")
print(f"Final state: {bg.status()}")
