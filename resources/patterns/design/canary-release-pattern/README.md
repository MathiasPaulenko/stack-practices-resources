# Canary Release Pattern — Runnable Implementations

Companion to the StackPractices pattern [Canary Release Pattern](https://stackpractices.com/patterns/canary-release-pattern/).

A canary release simulator in three equivalent implementations: a stage list (1% → 5% → 25% → 50% → 100%), a health-metric gate after each bake period, automatic rollback on the first failing stage and promotion when the canary reaches 100%. Stdlib only — no dependencies needed.

## Files

| File | Stack | Run |
| --- | --- | --- |
| `src/canary_release.py` | Python 3.9+ (stdlib only) | `python src/canary_release.py` |
| `src/canary-release.js` | Node.js 14+ (stdlib only) | `node src/canary-release.js` |
| `src/CanaryRelease.java` | Java 16+ (`record`, `var`, `Map.of`) | `javac src/CanaryRelease.java && java -cp src CanaryRelease` |

Each run advances through the stages and evaluates a mocked health check that returns degraded metrics on the third call, so you see the rollback path end to end. Edit `mock_health_check`/`mockHealthCheck` to always return healthy metrics and you'll get the full-promotion path instead.

The bake times are fractions of a second so the demo finishes instantly; in production each stage runs 5-30 minutes against real metrics (Prometheus, Datadog, etc.).
