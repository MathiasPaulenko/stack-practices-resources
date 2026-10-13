# Cross-Region Failover Test Template

An execution template for running a cross-region failover drill that produces evidence: roles, go/no-go gates, abort criteria, a timed failover/failback timeline, a post-test report, and a guarded Bash script for Aurora Global Database + Route 53.

Source article: [Cross-Region Failover Test Template](https://stackpractices.com/docs/cross-region-failover-template/)

## Files

- `failover-test-template.md` — blank template ready to fill per drill
- `failover-test-example.md` — the same template filled out for a `payments-api` drill, including a missed-RTO report
- `failover.sh` — executable failover script with `--dry-run`, operator confirmation, lag gating, and DNS convergence checks

## How to use

1. Copy `failover-test-template.md` into your runbook or incident tool and fill every bracketed value before the window opens.
2. Walk `failover.sh --dry-run` once during rehearsal; it prints every AWS action without executing it.
3. On test day, export the required variables and run `failover.sh`. It exits cleanly if the secondary health check or the replication-lag gate fails.
4. Soak the secondary for 30 minutes, then execute the failback section and attach the completed report to your change record.

For a planned drill on Aurora Global Database the script uses `switchover-global-cluster` (RPO 0). For unplanned recovery use `failover-global-cluster`; for a standalone cross-region read replica use `promote-read-replica-db-cluster`. See the article's script walkthrough for details.
