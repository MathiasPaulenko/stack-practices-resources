/**
 * Registry / Multiton — one instance per key, with a reset hook for tests.
 *
 * More useful than a single getInstance(): named singletons, lazy factories,
 * and a `reset()`/`clear()` so tests can start from a clean slate.
 */

class Registry {
  private static instances = new Map<string, unknown>();

  static get<T>(key: string, factory: () => T): T {
    if (!Registry.instances.has(key)) {
      Registry.instances.set(key, factory());
    }
    return Registry.instances.get(key) as T;
  }

  static reset(key: string): void {
    Registry.instances.delete(key);
  }

  static clear(): void {
    Registry.instances.clear();
  }
}

interface Pool {
  acquire(): string;
  size: number;
}

function createPool(): Pool {
  let n = 0;
  return {
    acquire: () => `conn-${++n}`,
    get size() {
      return n;
    },
  };
}

// --- demo ---
const a = Registry.get("db-pool", createPool);
const b = Registry.get("db-pool", createPool);
console.log("same instance:", a === b);
console.log("acquire:", a.acquire(), "| via other ref:", b.acquire());

// in tests: reset between cases so state doesn't leak
Registry.reset("db-pool");
const fresh = Registry.get("db-pool", createPool);
console.log("fresh after reset:", fresh !== a, "| size:", fresh.size);

export { Registry };
