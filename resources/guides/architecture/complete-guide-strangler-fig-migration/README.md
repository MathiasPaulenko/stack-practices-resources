# Strangler Fig Migration - Code Examples

Runnable TypeScript and Python examples from the guide:
<https://stackpractices.com/guides/complete-guide-strangler-fig-migration/>

## Files

| File | What it shows |
| --- | --- |
| `strangler_router.ts` | Application-level router: rule matching, feature-flag rollout, try/catch fallback to legacy |
| `shadow_traffic.ts` | Dark launch: parallel calls to both systems, key-field response comparison |
| `feature_flags.ts` | Percentage / user-list / environment / boolean rollout strategies with stable bucketing |
| `dual_write.ts` | Dual-write with new-system-first ordering and a retry queue for legacy failures |
| `rollback_manager.ts` | Automatic rollback on error-rate and p99-latency thresholds |
| `cdc_sync.py` | Debezium-style Kafka consumer replaying changes into the new store |
| `kong_routes.yaml` | Edge routing: path-based split between new service and legacy monolith |

## Notes

- The TypeScript files are library code — wire them to your HTTP framework's
  request/response types. `SystemAdapter` is the seam: implement it once for
  the legacy system and once for the new one.
- `cdc_sync.py` needs a running Kafka with a Debezium (or similar) connector
  publishing to `legacy-db-changes`. `pip install -r requirements.txt`.
- The guide explains why `isEnabled` must be awaited, why flag fields need
  `?.` guards, and why function definitions precede the consume loop — all
  three were real bugs in earlier drafts.
