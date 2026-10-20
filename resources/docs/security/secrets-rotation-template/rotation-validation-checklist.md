# Rotation Validation Checklist

Run after every secret rotation. Attach the completed copy to the rotation log.

## During the transition

- [ ] New secret generated and stored in the secret manager (never in chat or email)
- [ ] Application deployed with dual-read / both credentials valid
- [ ] Staging validation passed with the new secret
- [ ] All known consumers updated one by one
- [ ] Secret manager access logs reviewed for unknown consumers

## Before revoking the old secret

- [ ] New secret is readable by all expected services
- [ ] Application logs show no authentication failures post-rotation
- [ ] Batch jobs / cron workers ran at least once without failures
- [ ] CI/CD pipelines pass with new secret
- [ ] Monitoring alerts are green for 24–48 hours

## After revocation

- [ ] Old secret revoked / deleted (not just unused)
- [ ] Inventory updated with new version and rotation date
- [ ] Exception log updated if the interval was extended
- [ ] Runbook updated if the procedure changed
- [ ] Rotation event logged to SIEM / audit trail
