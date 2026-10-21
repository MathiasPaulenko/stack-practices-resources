# Consumer Migration Checklist — Breaking Change to v2

Track one of these per consumer team when a breaking schema change ships as a new versioned topic.

## Before migration

- [ ] v2 schema registered in the schema registry
- [ ] Compatibility check passed for the v2 subject
- [ ] v2 topic created with correct partitions, retention, and ACLs
- [ ] Migration deadline announced in consumer channels
- [ ] Consumer code updated to deserialize the v2 schema
- [ ] DLQ configured for unexpected or malformed messages during the transition

## During migration

- [ ] Producer deployed with dual-write to v1 and v2
- [ ] Consumer deployed and reading from v2
- [ ] Consumer lag on v2 reached zero
- [ ] No deserialization errors or DLQ growth on v2

## After migration

- [ ] Old consumer group deleted or confirmed idle
- [ ] v1 write path disabled once every consumer has migrated
- [ ] 30-day grace period elapsed with no v1 activity
- [ ] v1 topic deleted
- [ ] v1 subject deleted from the registry

## Rollback

If a consumer is found on v1 during the grace period: keep dual-writing, migrate that consumer, restart the countdown. If v1 was already deleted, recover via the DLQ/backfill — deleted topic history cannot be restored.
