"""Simulation of the five-phase dependency upgrade runbook.

Two upgrades run through the same checklist: one succeeds end to end,
one fails validation and exercises the rollback path.
"""

DEPS = [
    {"name": "requests", "current": "2.31.0", "target": "2.32.3", "breaks_tests": False},
    {"name": "left-pad-classic", "current": "1.0.0", "target": "2.0.0", "breaks_tests": True},
]


def run_phase(label: str, steps: list[str]) -> None:
    print(f"\n== {label} ==")
    for step in steps:
        print(f"  [done] {step}")


def upgrade(dep: dict) -> None:
    print(f"\n########## upgrade {dep['name']} {dep['current']} -> {dep['target']} ##########")

    run_phase("1. Preparation", [
        "changelog reviewed for breaking changes",
        f"branch created: deps/upgrade-{dep['name']}-{dep['target']}",
        "CI green on main",
    ])

    run_phase("2. Upgrade", [
        "version bumped in requirements.txt",
        "pip-compile resolved, no conflicts",
        f"tests run: {'2 FAILING' if dep['breaks_tests'] else 'all passing'}",
    ])

    stable = not dep["breaks_tests"]
    run_phase("3. Validation", [
        "coverage report reviewed",
        "no new warnings in logs",
        "pip-audit: 0 high/critical",
        f"result: {'STABLE' if stable else 'UNSTABLE'}",
    ])

    if not stable:
        run_phase("4. Rollback", [
            "git checkout pre-upgrade-tag -- requirements.in requirements.txt",
            "pip install restored last known good",
            "rollback executed in <15 min",
        ])
        print(f"  => {dep['name']} stays at {dep['current']}; upgrade rejected")
        return

    run_phase("5. Merge & Monitor", [
        "PR opened with changelog summary",
        "staging soak: 24h clean",
        "production deploy in low-traffic window",
        "error rate flat after 48h",
    ])
    print(f"  => {dep['name']} is now {dep['target']}")


if __name__ == "__main__":
    for dep in DEPS:
        upgrade(dep)
