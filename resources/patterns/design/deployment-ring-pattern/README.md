# Deployment Ring Pattern — Runnable Implementations

Companion code for the StackPractices pattern:
[Deployment Ring Pattern](https://stackpractices.com/patterns/deployment-ring-pattern/)

Progressive rollout through rings of increasing size (1% → 5% → 25% → 100%)
with a health gate between each stage. If a ring fails its gate, every
completed ring rolls back — not just the failed one.

## Files

| File | What it shows |
|------|---------------|
| `src/ring_deployment.py` | Python ring deployer with dataclasses, enum state machine and rollback |
| `src/ring-deployment.js` | The same logic in async JavaScript |
| `src/RingDeployment.java` | Java 16+ records version |
| `ring-config.yaml` | Example ring configuration: audiences, bake windows, health-gate thresholds, rollback policy |

## Run

```bash
python src/ring_deployment.py     # Python 3.8+
node src/ring-deployment.js       # Node 14+
javac src/RingDeployment.java && java -cp src RingDeployment   # Java 16+
```

All three run the same scenario: a mock health check fails on the third
call (ring 2 at 25%), so rings 0–1 complete and then roll back. Expected
ending output:

```text
FAIL - Ring 2 failed health check, rolling back
  Rolling back ring 1 (early-adopters)
  Rolling back ring 0 (internal)

Result: {'version': '2.1.0', 'status': 'rolled_back', 'failed_ring': 2, 'rings_completed': 2}
```

## Wiring it to a real system

Replace `mock_health_check` with a call to your metrics backend
(Prometheus, Datadog, CloudWatch) and route the ring percentages through
feature flags, load-balancer weights, or your service mesh. The
`ring-config.yaml` file mirrors the knobs the implementations expose.
