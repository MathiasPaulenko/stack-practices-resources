# Capacity Planning — Load Test and Bottleneck Analyzer

Companion code for the [Capacity Planning guide](https://stackpractices.com/guides/capacity-planning-guide/) on StackPractices.

## Files

- `src/capacity-test.js` — k6 load test with staged ramp (100 → 200 VUs) and p95/error-rate thresholds. Run with `k6 run capacity-test.js`; override the target with `BASE_URL=https://your.api`.
- `src/bottleneck_analyzer.py` — Python script that evaluates per-resource headroom against saturation thresholds and identifies which resource is your effective capacity ceiling. Run with `python bottleneck_analyzer.py`.

## Requirements

- Python 3.9+ (no dependencies beyond the standard library)
- [k6](https://k6.io/) for the load test
