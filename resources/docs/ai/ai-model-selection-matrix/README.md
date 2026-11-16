# AI Model Selection Matrix — Companion Files

Standalone files for the [AI Model Selection Matrix](https://stackpractices.com/docs/ai-model-selection-matrix/) doc on StackPractices. Copy what you need; each file works on its own.

## Files

| File | What it is |
|---|---|
| `model-pricing-comparison.csv` | Nine current models side by side: input/output price per 1K tokens, context window, multimodal support. |
| `cost-per-1000-queries.csv` | The same workload (1500 input + 500 output tokens per query) priced across all nine models — per query, per 1K queries, and monthly at 10K queries/day. |
| `weighted-scorecard-template.md` | The weighted decision scorecard: criteria, suggested weights, a filled example, and how to compute the winner. |
| `model-selection-checklist.md` | The pre-lock checklist: workload, benchmark, scorecard, TCO, latency, fallback, re-evaluation cadence. |

## Quick start

1. Update `model-pricing-comparison.csv` with current provider pricing — these rows are a snapshot.
2. Run your own benchmark (50–100 production inputs) on the top 2–3 candidates.
3. Fill the scorecard with weights that reflect your feature, not generic averages.
4. Walk the checklist before committing.

## Notes

- Prices drift fast — verify against provider pricing pages before locking.
- The scorecard won't make the call for you; it makes the trade-offs explicit.
