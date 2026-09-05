"""Staged rollout plan for gradually increasing flag percentage."""

rollout_plan = [
    {"percentage": 1, "duration_hours": 24},
    {"percentage": 5, "duration_hours": 48},
    {"percentage": 25, "duration_hours": 72},
    {"percentage": 50, "duration_hours": 96},
    {"percentage": 100, "duration_hours": 0},
]


def advance_rollout(flag: str, current_pct: int) -> int:
    """Advance to the next rollout stage.

    Returns the new percentage, or 100 if already at max.
    """
    for stage in rollout_plan:
        if stage["percentage"] > current_pct:
            print(f"Advancing {flag}: {current_pct}% -> {stage['percentage']}%")
            update_flag(flag, {"percentage": stage["percentage"]})
            return stage["percentage"]
    return 100


def update_flag(flag: str, rule: dict) -> None:
    """Placeholder for flag store update (Redis, DB, LaunchDarkly, etc.)."""
    print(f"[store] {flag} = {rule}")


if __name__ == "__main__":
    flag = "new_checkout"
    pct = 0
    for _ in range(len(rollout_plan)):
        pct = advance_rollout(flag, pct)
        if pct >= 100:
            print("Rollout complete.")
            break
