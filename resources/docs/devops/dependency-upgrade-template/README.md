# Dependency Upgrade Runbook — Runnable Simulation

Companion to the StackPractices doc [Dependency Upgrade Runbook](https://stackpractices.com/docs/dependency-upgrade-template/).

A simulation of the runbook's five phases in three languages. Each script walks two dependency upgrades through the same checklist: one passes validation and goes through merge and monitoring, the other fails its test phase and exercises the rollback path — tag restore, clean install, done in under 15 minutes. Stdlib only, no dependencies.

## Files

| File | Stack | Run |
| --- | --- | --- |
| `src/upgrade-runbook.js` | Node.js 18+ | `node src/upgrade-runbook.js` |
| `src/upgrade_runbook.py` | Python 3.9+ | `python src/upgrade_runbook.py` |
| `src/UpgradeRunbook.java` | Java 11+ | `javac -d src src/UpgradeRunbook.java && java -cp src UpgradeRunbook` |

Each run prints the checklist per phase — preparation, upgrade, validation, rollback, merge and monitor — so you can see exactly which steps gate a promotion and which trigger a revert. The tooling names are localized per stack (npm, pip-compile, mvn) to mirror a real runbook.
