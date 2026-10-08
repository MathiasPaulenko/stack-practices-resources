# System Decommissioning Checklist Template

Operational kit for retiring a production service without breaking downstream
consumers. Companion to the guide at
<https://stackpractices.com/docs/system-decommissioning-checklist-template/>.

## Files

| File | What it is |
| --- | --- |
| `decommissioning-checklist.md` | The full 7-phase checklist: discovery, data handling, dependency removal, shutdown, cleanup, documentation, verification. Copy it into your wiki or issue tracker and fill in the placeholders. |
| `decommissioning-notification.txt` | Notification email to send at T-30 (and resend at T-14 / T-3). |
| `post-decommissioning-audit.md` | The 30-day audit checklist — run it one full billing cycle after shutdown. |
| `verify-remaining-resources.sh` | Bash script that checks DNS, EC2, RDS, S3, ACM, and CloudWatch for leftovers tagged with the service name. Extend it for your stack. |

## Suggested order

1. Fill in `decommissioning-checklist.md` starting with section 1 (Discovery).
   Do not skip it — every decommissioning incident starts with an unmapped
   dependency.
2. Send `decommissioning-notification.txt` at T-30, resend at T-14 and T-3.
3. Stop the service in staging, watch 24-48 hours, then production.
4. During the 30-day window, run `verify-remaining-resources.sh` weekly:

   ```bash
   SERVICE_NAME=my-service AWS_REGION=us-east-1 ./verify-remaining-resources.sh
   ```

5. At T+30, complete `post-decommissioning-audit.md` and file it as evidence.
6. At T+90, purge retained artifacts per your retention policy.

## Notes

- Keep a restorable snapshot (repo archive, config export, data dump) for 90
  days — it makes a temporary restart cheap if a hidden consumer surfaces.
- "Archive" means a verified restore, not a copy. Test one file at T-14.
