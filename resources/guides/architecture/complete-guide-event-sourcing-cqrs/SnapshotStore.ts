// SnapshotStore.ts — Checkpoint aggregate state to skip long replays
class SnapshotStore {
  constructor(private readonly db: Database) {}

  
