# Blue-Green Deployment Pattern — Runnable Implementations

Companion to the StackPractices pattern [Blue-Green Deployment Pattern](https://stackpractices.com/patterns/blue-green-deployment-pattern/).

A blue-green deployment simulator in three equivalent implementations: two environments (blue/green), a smoke-test gate, an instant traffic switch and a one-step rollback to the previous version. Stdlib only — no dependencies needed.

## Files

| File | Stack | Run |
| --- | --- | --- |
| `src/blue_green_deployment.py` | Python 3.10+ (stdlib only) | `python src/blue_green_deployment.py` |
| `src/blue-green-deployment.js` | Node.js 18+ (stdlib only) | `node src/blue-green-deployment.js` |
| `src/BlueGreenDeployment.java` | Java 10+ (`var`, `Map.of`) | `javac src/BlueGreenDeployment.java && java -cp src BlueGreenDeployment` |

Each run deploys v2.0.0 to the idle environment, runs two smoke tests, switches traffic, then simulates an issue and rolls back — printing the state and deployment history at every step. Make one smoke test return `false` to see the failed-deploy path.
