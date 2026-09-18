"""Human-in-the-Loop gate for LLM agents — runnable companion code.

Companion to https://stackpractices.com/patterns/human-in-the-loop-pattern/

Implements the risk x confidence approval matrix and a unittest suite that
exercises auto-execution, review pause, rejection, and modification paths.

Run the tests:

    python -m unittest human_in_the_loop -v
"""

from __future__ import annotations

import unittest
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, Optional


class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ApprovalStatus(Enum):
    APPROVED = "approved"
    REJECTED = "rejected"
    MODIFIED = "modified"


@dataclass
class AgentAction:
    name: str
    description: str
    risk: RiskLevel
    parameters: Dict[str, Any] = field(default_factory=dict)
    confidence: float = 1.0


@dataclass
class ApprovalRequest:
    action: AgentAction
    reason: str
    agent_state: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ApprovalResponse:
    status: ApprovalStatus
    modified_parameters: Optional[Dict[str, Any]] = None
    feedback: str = ""


class HumanInTheLoop:
    def __init__(
        self,
        confidence_threshold: float = 0.7,
        auto_approve_low_risk: bool = True,
        reviewer: Optional[Callable[[ApprovalRequest], ApprovalResponse]] = None,
    ):
        self.confidence_threshold = confidence_threshold
        self.auto_approve_low_risk = auto_approve_low_risk
        self.reviewer = reviewer or self._default_reviewer

    def _default_reviewer(self, request: ApprovalRequest) -> ApprovalResponse:
        print(f"\n--- APPROVAL REQUIRED ---")
        print(f"Action: {request.action.name}")
        print(f"Description: {request.action.description}")
        print(f"Risk: {request.action.risk.value}")
        print(f"Confidence: {request.action.confidence:.0%}")
        print(f"Parameters: {request.action.parameters}")
        print(f"Reason: {request.reason}")
        print(f"-------------------------")

        choice = input("Approve? (y/n/m=modify): ").strip().lower()
        if choice == "y":
            return ApprovalResponse(status=ApprovalStatus.APPROVED)
        elif choice == "m":
            new_params = dict(request.action.parameters)
            key = input("Parameter to modify (or empty to skip): ").strip()
            if key and key in new_params:
                new_params[key] = input(f"New value for {key}: ").strip()
            return ApprovalResponse(
                status=ApprovalStatus.MODIFIED,
                modified_parameters=new_params,
            )
        return ApprovalResponse(
            status=ApprovalStatus.REJECTED, feedback="Rejected by reviewer"
        )

    def needs_approval(self, action: AgentAction) -> bool:
        if action.risk == RiskLevel.HIGH:
            return True
        if (
            action.risk == RiskLevel.MEDIUM
            and action.confidence < self.confidence_threshold
        ):
            return True
        if action.risk == RiskLevel.LOW and not self.auto_approve_low_risk:
            return True
        return False

    def execute_with_approval(
        self,
        action: AgentAction,
        execute_fn: Callable[[AgentAction], str],
        reason: str = "",
    ) -> str:
        if not self.needs_approval(action):
            return execute_fn(action)

        request = ApprovalRequest(action=action, reason=reason)
        response = self.reviewer(request)

        if response.status == ApprovalStatus.REJECTED:
            return f"[REJECTED] {action.name}: {response.feedback}"

        if (
            response.status == ApprovalStatus.MODIFIED
            and response.modified_parameters
        ):
            action.parameters = response.modified_parameters

        return execute_fn(action)


class TestNeedsApproval(unittest.TestCase):
    def setUp(self):
        self.hitl = HumanInTheLoop(confidence_threshold=0.7)

    def test_high_risk_always_needs_approval(self):
        a = AgentAction("deploy", "Deploy", RiskLevel.HIGH, {}, 0.99)
        self.assertTrue(self.hitl.needs_approval(a))

    def test_low_risk_auto_approved(self):
        a = AgentAction("read", "Read", RiskLevel.LOW, {}, 0.5)
        self.assertFalse(self.hitl.needs_approval(a))

    def test_low_risk_needs_approval_when_disabled(self):
        hitl = HumanInTheLoop(auto_approve_low_risk=False)
        a = AgentAction("read", "Read", RiskLevel.LOW, {}, 0.9)
        self.assertTrue(hitl.needs_approval(a))

    def test_medium_risk_below_threshold_needs_approval(self):
        a = AgentAction("delete", "Delete", RiskLevel.MEDIUM, {}, 0.5)
        self.assertTrue(self.hitl.needs_approval(a))

    def test_medium_risk_above_threshold_auto(self):
        a = AgentAction("delete", "Delete", RiskLevel.MEDIUM, {}, 0.9)
        self.assertFalse(self.hitl.needs_approval(a))


class TestExecuteWithApproval(unittest.TestCase):
    def test_auto_executes_low_risk(self):
        hitl = HumanInTheLoop()
        a = AgentAction("read", "Read", RiskLevel.LOW, {"path": "/x"})
        out = hitl.execute_with_approval(a, lambda act: f"ran {act.name}")
        self.assertEqual(out, "ran read")

    def test_rejection_returns_feedback(self):
        hitl = HumanInTheLoop(reviewer=lambda r: ApprovalResponse(
            ApprovalStatus.REJECTED, feedback="nope"))
        a = AgentAction("deploy", "Deploy", RiskLevel.HIGH, {})
        out = hitl.execute_with_approval(a, lambda act: "ran")
        self.assertIn("nope", out)

    def test_modification_applies_parameters(self):
        hitl = HumanInTheLoop(reviewer=lambda r: ApprovalResponse(
            ApprovalStatus.MODIFIED, modified_parameters={"env": "staging"}))
        a = AgentAction("deploy", "Deploy", RiskLevel.HIGH, {"env": "prod"})
        out = hitl.execute_with_approval(a, lambda act: f"env={act.parameters['env']}")
        self.assertEqual(out, "env=staging")

    def test_approval_executes(self):
        hitl = HumanInTheLoop(reviewer=lambda r: ApprovalResponse(
            ApprovalStatus.APPROVED))
        a = AgentAction("deploy", "Deploy", RiskLevel.HIGH, {})
        out = hitl.execute_with_approval(a, lambda act: "ran")
        self.assertEqual(out, "ran")


if __name__ == "__main__":
    unittest.main()
