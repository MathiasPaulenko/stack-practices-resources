import type { Repository } from "./repository.js";

/**
 * In-memory repository for fast, deterministic unit tests.
 * Uses a Map internally. No database required.
 */
export class InMemoryRepository<T extends { id: string }>
  implements Repository<T, string>
{
  private items: Map<string, T> = new Map();

  async findById(id: string): Promise<T | null> {
    return this.items.get(id) ?? null;
  }

  async findAll(filter?: Partial<T>): Promise<T[]> {
    const all = Array.from(this.items.values());
    if (!filter) return all;

    return all.filter((item) =>
      Object.entries(filter).every(
        ([key, value]) => (item as any)[key] === value,
      ),
    );
  }

  async create(data: Omit<T, "id">): Promise<T> {
    const id = crypto.randomUUID();
    const item = { id, ...data } as T;
    this.items.set(id, item);
    return item;
  }

  async update(id: string, data: Partial<T>): Promise<T | null> {
    const existing = this.items.get(id);
    if (!existing) return null;

    const updated = { ...existing, ...data, id } as T;
    this.items.set(id, updated);
    return updated;
  }

  async delete(id: string): Promise<boolean> {
    return this.items.delete(id);
  }
}
