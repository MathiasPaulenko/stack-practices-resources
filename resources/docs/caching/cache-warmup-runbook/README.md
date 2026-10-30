# Cache Warmup Runbook — Companion

Companion to the StackPractices doc [Cache Warmup Runbook](https://stackpractices.com/docs/cache-warmup-runbook/).

## Files

| File | Purpose | Run |
| --- | --- | --- |
| `src/hot_keys.py` | Builds `hot-keys.json` from JSONL access logs or Redis LFU stats (`OBJECT FREQ`), grouped by priority tier. | `python3 src/hot_keys.py --logs access.jsonl --output hot-keys.json` |
| `src/warmup.py` | Tiered warmup runner: health check, chunked batches with pauses, coverage verification. Ships with a `--demo` loader so it runs without a database. | `python3 src/warmup.py --keys hot-keys.json --redis localhost:6379 --demo` |
| `src/warmup-before-deploy.sh` | Deployment gate: extract → warm critical+high → verify instance. Exits non-zero on failure. | `REDIS_HOST=redis-new.internal ./src/warmup-before-deploy.sh` |
| `src/k8s-warmup-job.yaml` | One-shot Kubernetes `Job` that runs the warmup and self-cleans via `ttlSecondsAfterFinished`. | `kubectl apply -f src/k8s-warmup-job.yaml` |

## Requirements

- Python 3.10+ and `redis` (`pip install redis`) for the scripts.
- `redis-cli` on PATH for the verification step in the bash gate.
- For `--lfu` extraction: Redis 4.0+ with `maxmemory-policy` set to
  `allkeys-lfu` or `volatile-lfu`. Under LRU policies the frequency
  counter does not exist — use `--logs` instead.

## Usage

```bash
# 1. Extract hot keys grouped by tier (critical/high/medium/low)
python3 src/hot_keys.py --logs /var/log/app/cache-access.jsonl --output hot-keys.json
# or, with an LFU eviction policy:
python3 src/hot_keys.py --lfu --redis localhost:6379 --output hot-keys.json

# 2. Test the warmup flow against a local Redis with the demo loader
python3 src/warmup.py --keys hot-keys.json --redis localhost:6379 --demo

# 3. In production: edit warmup.py, replace demo_loader with a loader
#    that reads your source of truth, then gate the deploy:
./src/warmup-before-deploy.sh
```

The runner exits `0` when sampled coverage is ≥ 80% and `2` otherwise,
so a pipeline can block the traffic switch on a failed warmup — the same
gate the runbook describes.
