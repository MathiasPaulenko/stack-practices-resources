import { MultiLevelCache } from './multi-level-cache';

export class InstrumentedMultiLevelCache extends MultiLevelCache {
  private hits = { l1: 0, l2: 0, miss: 0 };

  async get<T>(key: string): Promise<T | undefined> {
    const l1Value = this.l1.get(key);
    if (l1Value !== undefined) {
      this.hits.l1++;
      return l1Value as T;
    }

    const l2Value = await this.l2.get(key);
    if (l2Value !== null) {
      this.hits.l2++;
      const parsed = JSON.parse(l2Value) as T;
      this.l1.set(key, parsed);
      return parsed;
    }

    this.hits.miss++;
    return undefined;
  }

  getHitRates() {
    const total = this.hits.l1 + this.hits.l2 + this.hits.miss;
    if (total === 0) return { l1: 0, l2: 0, miss: 0, total: 0 };
    return {
      l1: (this.hits.l1 / total * 100).toFixed(1) + '%',
      l2: (this.hits.l2 / total * 100).toFixed(1) + '%',
      miss: (this.hits.miss / total * 100).toFixed(1) + '%',
      total,
    };
  }

  resetStats() {
    this.hits = { l1: 0, l2: 0, miss: 0 };
  }
}
