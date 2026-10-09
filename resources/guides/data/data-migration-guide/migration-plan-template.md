# Migration Plan Template

Fill this in before touching production data.

## Goal
<!-- What changes, why, and the success criteria -->

## Timeline
<!-- Phases with dates; rollback window -->

## Phase 1 — Schema Changes
- [ ] New tables/columns added (nullable, no drops yet)
- [ ] Foreign keys in place
- [ ] Dual-write code deployed
- [ ] Writes verified on both systems

## Phase 2 — Backfill
- [ ] Batched script running (rows/batch: ___)
- [ ] Checkpoint table created
- [ ] Progress + error rate monitored
- [ ] Backfill complete + verified (counts, checksums)

## Phase 3 — Shadow Reads
- [ ] Parallel reads enabled
- [ ] Mismatch rate < 0.1%
- [ ] Discrepancies fixed or explained

## Phase 4 — Cutover
- [ ] Reads switched behind feature flag
- [ ] Error rates monitored 24h
- [ ] Writes switched
- [ ] Dual-write code removed (after rollback window)
- [ ] Old columns/tables dropped

## Validation
- [ ] Row counts match
- [ ] Field-by-field sample (n = ___)
- [ ] Aggregate checksums equal
- [ ] Integration tests pass
- [ ] Performance acceptable under load

## Rollback Plan
- [ ] Inside window: feature flag off → reads back to old schema
- [ ] Outside window: forward-fix migration plan
