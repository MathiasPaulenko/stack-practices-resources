# DR Test Calendar

Set the exercise cadence from service risk, recovery objectives, change rate, and applicable requirements. A quarterly rotation is one possible schedule, not a universal rule.

| Quarter | Scenario | Owner | Target RTO | Last Tested |
|---------|----------|-------|------------|-------------|
| `<period>` | `<scenario>` | `<owner>` | `<approved target>` | `<date or pending>` |
| `<period>` | `<scenario>` | `<owner>` | `<approved target>` | `<date or pending>` |
| `<period>` | `<scenario>` | `<owner>` | `<approved target>` | `<date or pending>` |
| `<period>` | `<scenario>` | `<owner>` | `<approved target>` | `<date or pending>` |

## Cadence rules

1. **Walk the timeline on paper first.** Run a tabletop pass over the execution schedule before touching infrastructure — gaps in ownership and access show up for free.
2. **Include third-party dependency tests.** DR depends on DNS providers, CDNs, and external APIs. Run `dependency-checks.sh` during every cutover.
3. **One named test lead per drill.** Rotating ownership between exercises is fine; a test without a single accountable lead produces a report nobody reads.
4. **After any infrastructure change**, schedule a targeted drill for the changed component instead of waiting for the next scheduled exercise.

## Tracking sheet

Copy this row into your tracker after each test and link the post-test report:

| Date | Scenario | RTO target | RTO actual | RPO target | RPO actual | Result | Report link |
|------|----------|-----------:|-----------:|-----------:|-----------:|--------|-------------|
| ____ | ________ | __________ | __________ | __________ | __________ | P/F    | __________ |
