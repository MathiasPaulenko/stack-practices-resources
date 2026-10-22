# System Design Interview — Companion Artifacts

Companion files for [System Design Interview: Framework, Examples & Practice](https://stackpractices.com/guides/system-design-interview-guide/).

These artifacts support the worked URL shortener example so you can rehearse
the capacity math and inspect the schemas instead of only reading them.

## Files

- `capacity_estimator.py` — prints writes/s, reads/s, R/W ratio and storage
  projections from daily volumes. Run it, then change the inputs and
  explain out loud how the architecture would change.
- `schema.sql` — PostgreSQL table for the URL mapping (write path, OLTP).
- `click_events.cql` — Cassandra table for append-only click analytics.
- `api.http` — the three-endpoint API contract (shorten, redirect, stats)
  in REST Client format.

## Usage

```bash
python capacity_estimator.py
# Writes : 100,000,000/day  ≈ 1,157/s (peak ~3,472/s)
# Reads  : 10,000,000,000/day  ≈ 115,741/s (peak ~347,222/s)
# R/W ratio: 100:1
# Storage: 60 GB/day ≈ 22 TB/year (~110 TB over 5 years)
```

Feed your own numbers when practicing other problems: the habit of
quantifying before drawing boxes is the skill being rehearsed.
