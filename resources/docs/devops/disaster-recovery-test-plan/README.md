# Disaster Recovery Test Plan — Companion Kit

Standalone files from the [Disaster Recovery Test Plan](https://stackpractices.com/docs/disaster-recovery-test-plan/) template on StackPractices. Everything here is meant to be copied into your own repo and adapted.

## Contents

| File | What it is |
|------|-----------|
| `dr-test-plan-template.md` | Six-section test plan: objectives, scope, scenarios, execution timeline, data integrity, post-test report with sign-off |
| `dr_test_runner.py` | boto3-based runner that restores an RDS snapshot in the DR region, runs smoke tests, checks data integrity, and measures real RTO |
| `game-day.sh` | Chaos engineering script with `network`, `disk`, `cpu`, and `full` failure scenarios against a Kubernetes cluster |
| `dependency-checks.sh` | DNS, CDN, and external-API circuit-breaker checks to run after cutover |
| `integrity-checks.sql` | Transaction count, checksum, replication-lag, and RTO/RPO tracking queries |
| `dr-test-calendar.md` | Quarterly scenario rotation with cadence rules and a tracking sheet |

## Usage

```bash
# Bash syntax check before running anything destructive
bash -n game-day.sh

# Python syntax check
python -m py_compile dr_test_runner.py
```

**Warning:** `game-day.sh --scenario full` cordons and drains every node carrying the primary-region label. Run it only on clusters you can afford to take down, and never as a first drill.

The `DRTestRunner` expects AWS credentials with permission to restore RDS snapshots in the DR region, `psql` on PATH for the integrity query, and `kubectl` configured for game-day scenarios.

Source: [stackpractices.com/docs/disaster-recovery-test-plan](https://stackpractices.com/docs/disaster-recovery-test-plan/)
