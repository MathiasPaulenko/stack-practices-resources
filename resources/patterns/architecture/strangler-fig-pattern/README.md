# Strangler Fig Pattern — Companion Code

Runnable examples from [Strangler Fig: Gradually Replace Legacy by Intercepting](https://stackpractices.com/patterns/strangler-fig-pattern/) on StackPractices.

## Files

| File | What it shows |
|---|---|
| `nginx.conf` | Reverse proxy routing: migrated paths to the new service, everything else to legacy |
| `strangler_router.py` | Flask feature-flag router with canary percentage and an observability header |
| `StranglerGateway.java` | Spring Cloud Gateway route definitions for the same split |
| `shadow_traffic.py` | Sends requests to both systems, returns the legacy response, logs differences |
| `cutover.py` | Tracks per-route migration status and reports cutover readiness |
| `branch_by_abstraction.py` | Swaps implementations behind a common interface via a flag |
| `parallel_run.py` | Runs the same operation on both systems and records mismatches |

## Usage

- `strangler_router.py` needs `LEGACY_URL` and `NEW_SERVICE_URL` env vars plus `flask` and `requests`.
- `shadow_traffic.py` and `cutover.py` are dependency-free except for `requests`.
- `StranglerGateway.java` requires Spring Cloud Gateway on the classpath.
- `nginx.conf` drops into a standard Nginx `conf.d` layout.
