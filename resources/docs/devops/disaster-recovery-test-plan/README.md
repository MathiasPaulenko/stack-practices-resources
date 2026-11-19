# Disaster Recovery Test Plan — Companion Kit

Standalone files from the [Disaster Recovery Test Plan](https://stackpractices.com/docs/disaster-recovery-test-plan/) template on StackPractices. Everything here is meant to be copied into your own repo and adapted.

## Contents

| File | What it is |
|------|-----------|
| `dr-test-plan-template.md` | Six-section test plan: objectives, scope, scenarios, execution timeline, data integrity, post-test report with sign-off |
| `dr_test_runner.py` | Restores an RDS snapshot already available in the DR Region, tests a separate app URL, compares row counts, records RTO after app checks, and leaves RPO unset |
| `game-day.sh` | Controlled Kubernetes failure drills with dry-run default, explicit execution flag, named context, and cleanup handlers |
| `dependency-checks.sh` | DNS, CDN, and external-API circuit-breaker checks to run after cutover |
| `integrity-checks.sql` | PostgreSQL reporting queries for exported replication metrics and recorded DR test results |
| `dr-test-calendar.md` | Quarterly scenario rotation with cadence rules and a tracking sheet |

## Usage

Set `KUBE_CONTEXT` to a dedicated test cluster. The first command is a dry run; add `--execute` only after reviewing the target and scope. The `full` scenario also requires `PRIMARY_REGION` and a typed confirmation. The `disk` scenario requires a `FILL_SIZE` chosen for the test filesystem.

```bash
KUBE_CONTEXT="replace-with-test-context" ./game-day.sh --scenario network
KUBE_CONTEXT="replace-with-test-context" ./game-day.sh --scenario network --execute
```


```bash
# Bash syntax check before running anything destructive
bash -n game-day.sh

# Python syntax check
python -m py_compile dr_test_runner.py
```

**Warning:** `game-day.sh --scenario full` cordons and drains every node carrying the primary-region label. Run it only on clusters you can afford to take down, and never as a first drill.

Before running `DRTestRunner`, copy the RDS snapshot to the destination Region and wait until it is available. Supply AWS credentials, the destination DB subnet group, an isolated application test URL, and database connection URLs through approved configuration or a secret manager. The runner compares row counts only; it does not calculate RPO. `psql` must be on PATH, and `kubectl` must target a cluster approved for the game-day scenario.

Source: [stackpractices.com/docs/disaster-recovery-test-plan](https://stackpractices.com/docs/disaster-recovery-test-plan/)
