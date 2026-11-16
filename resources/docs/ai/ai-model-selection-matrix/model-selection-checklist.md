# Model Selection Checklist

Before locking a model for a feature:

- [ ] Workload measured — real tokens, real requests/day, real task mix
- [ ] Own benchmark run — 50+ production inputs on the top 2 candidates
- [ ] Scorecard filled — weights reflect this feature, not generic averages
- [ ] TCO calculated — retries, system prompt tokens, failed outputs
- [ ] Latency budget confirmed — p50 and p95 against the product requirement
- [ ] Fallback defined — secondary model + routing rule
- [ ] Re-evaluation scheduled — quarterly, plus triggers (new flagship, price cut on your tier, spend crossing a round number, open-weight release entering the top tier)

Keep the filled checklist next to the scorecard — six months from now it's the fastest way to explain why the incumbent still earns its place.
