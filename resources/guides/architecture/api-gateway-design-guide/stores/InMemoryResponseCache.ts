import { ResponseCacheStore } from '../middleware/cache';

interface Entry {
  status: number;
  body: unknown;
  headers: Record<string, string>;
  expiresAt: number;
}

export class InMemoryResponseCache implements ResponseCacheStore {
  private entries = new Map<string, Entry>();

  async get(key: string) {
    const entry = this.entries.get(key);
    if (!entry || entry.expiresAt < Date.now()) return null;
    return { status: entry.status, body: entry.body, headers: entry.headers };
  }

  async set(key: string, value: { status: number; body: unknown; headers: Record<string, string> }, ttlSeconds: number) {
    this.entries.set(key, { ...value, expiresAt: Date.now() + ttlSeconds * 1000 });
  }
}
