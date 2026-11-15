# Load Testing APIs with k6 — Companion Resources

Runnable k6 scripts for the [Load Testing APIs with k6 and Threshold-Based Assertions](https://stackpractices.com/recipes/load-testing-k6/) recipe.

## Contents

| File | What it does |
|------|--------------|
| `basic.js` | Staged ramp (100→200 VUs) with composite thresholds and `abortOnFail` |
| `scenario.js` | `ramping-arrival-rate` open-model scenario targeting 100→300 RPS, per-tag thresholds |
| `authenticated.js` | OAuth2 client-credentials login in `setup()`, cart → checkout flow |
| `data.js` + `users.csv` | `SharedArray`-parsed CSV test data distributed across VUs |
| `smoke.js` | 1 VU / 1 iteration CI gate with strict thresholds |
| `load-test-ci.yml` | GitHub Actions: smoke per PR, full load on `workflow_dispatch` |

## Usage

```bash
# install k6: https://k6.io/docs/get-started/installation/

# smoke test
k6 run --env BASE_URL=https://staging.example.com smoke.js

# staged load test
k6 run --env BASE_URL=https://staging.example.com basic.js

# arrival-rate scenario
k6 run --env BASE_URL=https://staging.example.com scenario.js

# authenticated flow
k6 run --env BASE_URL=https://staging.example.com \
     --env CLIENT_ID=x --env CLIENT_SECRET=y authenticated.js

# CSV-driven logins
k6 run --env BASE_URL=https://staging.example.com data.js

# metrics to Prometheus remote write
k6 run -o experimental-prometheus-rw basic.js
```

## Notes

- Point everything at staging — never production.
- Threshold breaches exit non-zero; that's what makes these scripts CI gates.
- Watch `dropped_iterations` in arrival-rate runs: it means the generator can't hold the target RPS and results flatter the API.
