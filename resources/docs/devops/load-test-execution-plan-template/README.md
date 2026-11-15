# Load Test Execution Plan Template — Companion Files

Files that go with the [Load Test Execution Plan Template](https://stackpractices.com/docs/load-test-execution-plan-template/) on StackPractices.

## Contents

- `load-test-execution-plan-template.md` — the fillable template: goals and scope, scenarios, success criteria, environment setup, the T-minus execution timeline, results, and findings with owners.
- `execution-checklist.md` — a printable day-of-the-test checklist, from T-1 day through the post-test steps.
- `k6-load-test.js` — a runnable k6 script that ramps to the peak scenario's virtual user count, tags requests with a correlation ID, and gates the run on a custom failure-rate metric.
- `locustfile.py` — the same scenario mix as a Locust `HttpUser` with weighted tasks; run with `locust -f locustfile.py --host <target>`.

## Usage

1. Copy `load-test-execution-plan-template.md` into your team's docs and fill every row.
2. Walk `execution-checklist.md` in order during the test window.
3. Adapt `k6-load-test.js` to your endpoints, then run `k6 run k6-load-test.js`.

The [Load Test Plan Template](https://stackpractices.com/docs/load-test-plan-template/) defines the objectives and thresholds this plan executes against; the [Load Test Report Template](https://stackpractices.com/docs/load-test-report-template/) is where the findings get filed.
