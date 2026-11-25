// Registry Pattern: central map of named instances and lazy factories.
// Run: node registry.js

class Registry {
  static #instances = new Map();
  static #factories = new Map();

  static register(name, instance) {
    Registry.#instances.set(name, instance);
  }

  static registerFactory(name, factory) {
    Registry.#factories.set(name, factory);
  }

  static get(name) {
    if (Registry.#instances.has(name)) {
      return Registry.#instances.get(name);
    }
    if (Registry.#factories.has(name)) {
      const instance = Registry.#factories.get(name)();
      Registry.#instances.set(name, instance);
      return instance;
    }
    throw new Error(`No registration found for: ${name}`);
  }

  static has(name) {
    return Registry.#instances.has(name) || Registry.#factories.has(name);
  }

  static reset() {
    // Clear everything — call this between tests to avoid state leakage.
    Registry.#instances.clear();
    Registry.#factories.clear();
  }
}

class DatabaseConnection {
  query(sql) {
    return `Result: ${sql}`;
  }
}

class CacheClient {
  get(key) {
    return `cached-${key}`;
  }
}

Registry.register('db', new DatabaseConnection());
Registry.registerFactory('cache', () => new CacheClient());

const db = Registry.get('db');
const cache = Registry.get('cache'); // factory runs here, then the instance is cached

console.log(db.query('SELECT 1'));
console.log(cache.get('users'));
console.log('has db:', Registry.has('db'));
console.log('same cache instance:', Registry.get('cache') === cache);

try {
  Registry.get('missing');
} catch (error) {
  console.log('Error:', error.message);
}
