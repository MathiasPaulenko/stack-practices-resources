# Load Testing APIs with k6 and JMeter

Runnable companion files for the [Load Testing recipe](https://stackpractices.com/recipes/load-testing/) on StackPractices.

## Contents

| File | What it is |
|------|-----------|
| `k6-load-test.js` | Baseline k6 script: staged ramp (100→200 VUs), p95/error-rate thresholds |
| `k6-advanced.js` | Advanced k6 script: `setup()` token reuse, `SharedArray` CSV data, weighted browsing/shopping/checkout scenarios, `abortOnFail` threshold |
| `users.csv` | Sample credential file consumed by `k6-advanced.js` |
| `jmeter-test-plan.jmx` | Complete JMeter test plan: 100 threads, 60s ramp, 5 min duration, response assertion |
| `load-test-ci.yml` | GitHub Actions pipeline: PR smoke test + release-branch full run |
| `load-test-checklist.md` | Pre-flight checklist for target, generator, script, and post-run |

## Quick start

```bash
# Baseline run
k6 run k6-load-test.js

# Point at a real target
BASE_URL=https://staging.example.com k6 run k6-load-test.js

# Advanced scenario (needs CLIENT_SECRET for the OAuth token request)
BASE_URL=https://staging.example.com CLIENT_SECRET=xxx k6 run k6-advanced.js

# JMeter, headless
jmeter -n -t jmeter-test-plan.jmx -l results.jtl
```

Read `load-test-checklist.md` before pointing any of this at a shared environment.
