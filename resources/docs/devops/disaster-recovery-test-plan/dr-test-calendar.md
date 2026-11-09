# DR Test Calendar

Rotating quarterly scenarios keep every failure mode exercised within a 12-month window.

| Quarter | Scenario | Owner | Target RTO | Last Tested |
|---------|----------|-------|------------|-------------|
| Q1 | Primary region failure | Platform team | 4 hours | ______ |
| Q2 | Database corruption | DBA team | 2 hours | ______ |
| Q3 | Network partition | Network team | 1 hour | ______ |
| Q4 | Full region + backup restore | SRE team | 8 hours | ______ |

## Cadence rules

1. **Walk the timeline on paper first.** Run a tabletop pass over the execution schedule before touching infrastructure — gaps in ownership and access show up for free.
2. **Include third-party dependency tests.** DR depends on DNS providers, CDNs, and external APIs. Run `dependency-checks.sh` during every cutover.
3. **One named test lead per drill.** Rotating ownership between quarters is fine; a test without a single accountable lead produces a report nobody reads.
4. **After any infrastructure change**, schedule a targeted drill for the changed component instead of waiting for the next quarter.

## Tracking sheet

Copy this row into your tracker after each test and link the post-test report:

| Date | Scenario | RTO target | RTO actual | RPO target | RPO actual | Result | Report link |
|------|----------|-----------:|-----------:|-----------:|-----------:|--------|-------------|
| ____ | ________ | __________ | __________ | __________ | __________ | P/F    | __________ |
