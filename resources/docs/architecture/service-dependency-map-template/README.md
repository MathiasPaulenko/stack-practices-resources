# Service Dependency Map Template

Downloadable companion to the doc
[Service Dependency Map Template](https://stackpractices.com/docs/service-dependency-map-template/).

A fillable dependency map for one service, plus the operational pieces
that keep it alive: OTel servicegraph config for auto-discovery, circuit
breaker presets, a structured health-check payload, and a static import
discovery script.

## Files

| File | Purpose |
|---|---|
| `dependency-map-template.md` | The blank 7-section template, ready to copy into a service repo |
| `dependency-map-filled-example.md` | The same template filled in for a real `checkout-service`, including a transitive dependency (`fraud-service` via `payment-service`) |
| `otel-servicegraph.yaml` | OpenTelemetry Collector config exporting caller-callee metrics for auto-discovery |
| `circuit-breakers.yaml` | Per-dependency circuit breaker presets keyed to the map's criticality flags |
| `health-check.json` | Structured dependency health payload (degraded example) |
| `discover_imports.py` | Static analysis script that lists a Python project's import dependencies |

## How to use

1. Copy `dependency-map-template.md` into the service's repo (README or
   `docs/` folder) and fill each section honestly — the fallback column
   describes what the service does *today*, not the plan.
2. Reconcile monthly against `otel-servicegraph.yaml` metrics: any
   `(client, server)` pair in traces but missing from the map is drift.
3. Wire `circuit-breakers.yaml` values into your resilience layer
   (Resilience4j, Polly, Istio DestinationRules).
4. Serve a payload shaped like `health-check.json` from your health
   endpoint; `200` when healthy, `503` only for critical-path failures.
