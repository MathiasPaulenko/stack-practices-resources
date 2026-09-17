# Serverless Cost Estimation Template — Companion Resources

Companion files for the [Serverless Cost Estimation Template](https://stackpractices.com/docs/serverless-cost-estimation-template/) on StackPractices.com.

## What's included

| File | Format | Description |
|------|--------|-------------|
| `cost-estimation.md` | Markdown | Standalone estimation worksheet: function profile, cost breakdown, hidden costs, scenario summary, validation log |
| `estimate-costs.py` | Python 3 | Lambda monthly cost calculator: single function via CLI flags or a multi-function JSON workload file; supports x86 and arm64 pricing |

## Quick start

### Single function

```bash
python estimate-costs.py --invocations 10000000 --duration-ms 200 --memory-mb 512
```

### Multiple functions

```bash
python estimate-costs.py workloads.json
```

```json
[
  {"name": "processOrder", "invocations": 10000000, "duration_ms": 200,
   "memory_mb": 512, "pc_gb_seconds": 0, "data_out_gb": 5},
  {"name": "webhookHandler", "invocations": 50000000, "duration_ms": 50,
   "memory_mb": 128}
]
```

## Adapt before production

1. Verify the `PRICE_*` constants against [AWS Lambda pricing](https://aws.amazon.com/lambda/pricing/) — rates change without notice.
2. Feed duration and invocation numbers from load tests, not guesses; model 3x and 10x scenarios.
3. Add the hidden-cost rows (logs, NAT, queues) to the estimate — they routinely account for a third of the bill.
4. Reconcile the estimate against Cost Explorer every month and update the validation log.
