# Human-in-the-Loop Pattern — Companion Code

Runnable version of the approval gate from the
[Human-in-the-Loop Pattern](https://stackpractices.com/patterns/human-in-the-loop-pattern/)
on StackPractices.

## Files

| File | Description |
|------|-------------|
| `human_in_the_loop.py` | `HumanInTheLoop` gate with `RiskLevel` x confidence matrix, pluggable `reviewer` callback, and a `unittest` suite covering every approval path |

## Requirements

- Python 3.10+ — no external dependencies.

## Usage

```python
from human_in_the_loop import (
    AgentAction, HumanInTheLoop, RiskLevel,
)

hitl = HumanInTheLoop(confidence_threshold=0.8)

action = AgentAction(
    "deploy", "Deploy to production", RiskLevel.HIGH,
    {"env": "prod", "version": "v2.1.0"}, 0.6,
)

result = hitl.execute_with_approval(action, real_deploy_fn, "release step")
```

## Approval matrix

| Risk | Confidence | Decision |
|------|------------|----------|
| HIGH | any | always pauses for review |
| MEDIUM | < threshold | pauses for review |
| MEDIUM | >= threshold | auto-executes |
| LOW | any | auto-executes (unless `auto_approve_low_risk=False`) |

## Notes

- The default reviewer is an interactive CLI prompt; inject any callable to
  route approvals to Slack, a web UI, or a secondary LLM.
- `ApprovalStatus.MODIFIED` lets the reviewer adjust parameters before the
  action runs — the modified dict replaces `action.parameters`.
- Rejections return feedback text instead of executing, so the agent can
  adapt its plan.
