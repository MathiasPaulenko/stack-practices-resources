# Load Test Plan Template — Companion Files

Ready-to-run files accompanying the StackPractices doc:
<https://stackpractices.com/docs/load-test-plan-template/>

## Contents

| Path | What it shows |
|------|---------------|
| `load-test-plan-template.md` | The fillable plan document: objectives, scope, journeys, load profiles, thresholds, monitoring, reporting |
| `k6-load-test.js` | k6 script implementing the three example journeys with stages, thresholds, and custom metrics |
| `load-test-plan.jmx` | JMeter test plan (JMX): 200 threads, 300s ramp-up, homepage sampler with status-200 assertion |
| `locustfile.py` | Locust file with weighted tasks (`@task`) matching the journey traffic mix |
| `report-template.md` | One-page load test report: configuration, results summary, bottlenecks, recommendations |

## Run

```bash
# k6
k6 run k6-load-test.js

# Locust (headless, 200 users, 34 min)
locust -f locustfile.py --headless -u 200 -r 30 -t 34m --host https://staging.example.com

# JMeter (GUI mode for editing, CLI for execution)
jmeter -n -t load-test-plan.jmx -l results.jtl -e -o report/
```

Replace `staging.example.com` with your environment and adjust the traffic mix, data, and thresholds to match §2–§4 of the plan document.
