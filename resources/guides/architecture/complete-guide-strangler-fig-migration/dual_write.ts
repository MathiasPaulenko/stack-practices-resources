// sync/DualWriter.ts — Write to both systems during migration
interface UserData {
  id: string;
  email: string;
  [key: string]: unknown;
}

interface Repository {
  saveUser(userData: UserData): Promise<void>;
}

interface RetryQueue {
  enqueue(jobType: string, payload: unknown): Promise<void>;
}

type SyncMode = 'dual-write' | 'new-only' | 'legacy-only';

class DualWriter {
  constructor(
    private readonly legacyRepo: Repository,
    private readonly newRepo: Repository,
    private readonly retryQueue: RetryQueue,
    private readonly syncMode: SyncMode,
  ) {}

  async saveUser(userData: UserData): Promise<void> {
    switch (this.syncMode) {
      case 'dual-write':
        // Write to both — new system is source of truth eventually
        await this.newRepo.saveUser(userData);
        try {
          await this.legacyRepo.saveUser(userData);
        } catch (error) {
          // Non-blocking — but queue it for reconciliation, don't just log it.
          // A silent failed write is silent data drift.
          console.error('Legacy write failed (non-blocking):', error);
          await this.retryQueue.enqueue('legacy-write', userData);
        }
        break;

      case 'new-only':
        await this.newRepo.saveUser(userData);
        break;

      case 'legacy-only':
        await this.legacyRepo.saveUser(userData);
        break;
    }
  }
}

// Migration phases:
// Phase 1: legacy-only (before migration starts)
// Phase 2: dual-write (both systems receive writes)
// Phase 3: new-only (legacy is read-only, then decommissioned)

export { DualWriter };
export type { UserData, Repository, RetryQueue, SyncMode };
