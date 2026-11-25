# Retry Backoff — Companion Resources

Runnable versions of the advanced retry techniques from the
[Retry Backoff recipe](https://stackpractices.com/recipes/retry-backoff/):
budgets, deadlines, and hedged requests.

## Files

| File | Language | What it demonstrates |
|---|---|---|
| `retry_budget.go` | Go | Token-bucket retry budget — caps retry traffic per second so a partial outage doesn't turn into self-inflicted DDoS |
| `hedged_request.ts` | TypeScript | Hedged request with cancellation — fires a duplicate after a delay, first response wins, loser is aborted |
| `retry_deadline.py` | Python | Context-aware retry decorator — stops when a wall-clock deadline is hit and never sleeps past it |

## Quick start

```bash
# Go (no deps)
go run retry_budget.go

# TypeScript (Deno or tsx)
npx tsx hedged_request.ts

# Python
pip install requests
python retry_deadline.py
```

Each snippet is self-contained — copy it into your codebase and adapt
the retryable-error predicate to your transport.
