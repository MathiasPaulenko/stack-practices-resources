"""Error budget and burn rate calculator.

Companion script for the SLA definition template. Compute the error
budget for an SLO target and the current burn rate from observed
error minutes, then map the result to a deploy policy action.
"""

from dataclasses import dataclass


@dataclass
class BudgetStatus:
    error_budget: float
    actual_error_rate: float
    burn_rate: float
    budget_remaining_pct: float
    action: str


def calculate_burn_rate(
    errors_minutes: float,
    total_minutes: float,
    slo_target: float,
) -> float:
    """Return the burn rate: actual error rate / allowed error rate."""
    error_budget = 1.0 - slo_target
    actual_error_rate = errors_minutes / total_minutes
    return actual_error_rate / error_budget


def budget_status(
    errors_minutes: float,
    total_minutes: float,
    window_minutes: float,
    slo_target: float,
) -> BudgetStatus:
    """Compute remaining error budget and the recommended action.

    errors_minutes: downtime/error minutes observed in the window so far.
    total_minutes: elapsed minutes in the window so far.
    window_minutes: full measurement window (e.g. 30 days = 43200).
    slo_target: e.g. 0.999 for 99.9%.
    """
    error_budget = 1.0 - slo_target
    budget_minutes = window_minutes * error_budget
    remaining = max(0.0, (budget_minutes - errors_minutes) / budget_minutes)
    burn = calculate_burn_rate(errors_minutes, total_minutes, slo_target)

    if remaining <= 0:
        action = "freeze-all + postmortem"
    elif remaining < 0.10:
        action = "freeze non-critical deploys"
    elif remaining < 0.25:
        action = "prioritize reliability work"
    elif remaining < 0.50:
        action = "proceed with caution"
    else:
        action = "ship freely"

    return BudgetStatus(
        error_budget=error_budget,
        actual_error_rate=errors_minutes / total_minutes,
        burn_rate=burn,
        budget_remaining_pct=remaining * 100,
        action=action,
    )


if __name__ == "__main__":
    # 20 min of downtime in 1 day, 99.9% SLO, 30-day window
    status = budget_status(
        errors_minutes=20,
        total_minutes=1440,
        window_minutes=43200,
        slo_target=0.999,
    )
    print(f"Burn rate: {status.burn_rate:.1f}x")
    print(f"Budget remaining: {status.budget_remaining_pct:.1f}%")
    print(f"Action: {status.action}")
