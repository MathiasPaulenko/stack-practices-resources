import { TokenBucketStore } from '../middleware/rateLimit';

export class InMemoryTokenBucketStore implements TokenBucketStore {
  private entries = new Map<string, { tokens: number; lastRefill: number; expiresAt: number }>();

  async get(key: string) {
    const entry = this.entries.get(key);
    if (!entry || entry.expiresAt < Date.now()) return null;
    return { tokens: entry.tokens, lastRefill: entry.lastRefill };
  }

  async set(key: string, tokens: number, lastRefill: number, ttlSeconds: number) {
    this.entries.set(key, { tokens, lastRefill, expiresAt: Date.now() + ttlSeconds * 1000 });
  }
}
