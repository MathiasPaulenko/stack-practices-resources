# Weighted Model Scorecard

Use this when two models look equivalent on paper. Assign each criterion a weight that reflects your actual traffic — latency doesn't matter for a nightly batch job, and cost doesn't matter for a page that runs twice a day.

## Scorecard

Score each cell 1–10, multiply by the weight, and sum per column. The example below is filled for a cost-sensitive workload with compliance constraints — replace candidates and weights with yours.

| Criterion | Weight | [Candidate 1] | [Candidate 2] | [Candidate 3] | Weighted best |
|---|---|---|---|---|---|
| Accuracy | 30% | 9/10 | 9/10 | 7/10 | tie |
| Cost per query | 25% | 6/10 | 5/10 | 9/10 | [Candidate 3] |
| Latency | 20% | 7/10 | 6/10 | 5/10 | [Candidate 1] |
| Context window | 10% | 7/10 | 6/10 | 10/10 | [Candidate 3] |
| Tool reliability | 10% | 8/10 | 9/10 | 6/10 | [Candidate 2] |
| Data control | 5% | 3/10 | 3/10 | 10/10 | [Candidate 3] |

## Criteria to consider

- **Accuracy** — score from your own benchmark (50–100 production inputs), not vendor leaderboards.
- **Cost per query** — input + output tokens on your real workload, plus ~30% for retries and failed outputs.
- **Latency** — p50 and p95 against the product requirement, not the average.
- **Context window** — headroom for your longest realistic input plus retrieved context.
- **Tool reliability** — valid tool calls per 100 attempts on your agent workload.
- **Data control** — residency, retention policy, ability to self-host if required.

## Example result

With the weights above, the open-weight candidate edges the total (7.45 vs 7.25 vs 6.80): cost and data control carry it despite weaker accuracy and latency rows. Keep the filled scorecard — it is the fastest way to answer "why this model?" when a stakeholder asks six months later.
