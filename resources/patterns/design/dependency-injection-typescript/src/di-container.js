// DI container with explicit lifetimes — JavaScript port of the article's
// TypeScript container. Factories wire the graph; lifetimes decide caching.

const Lifetime = Object.freeze({ Singleton: "singleton", Transient: "transient" });

class Container {
  constructor() {
    this.registrations = new Map();
    this.singletons = new Map();
  }

  register(token, factory, lifetime = Lifetime.Transient) {
    this.registrations.set(token, { factory, lifetime });
    return this;
  }

  resolve(token) {
    const reg = this.registrations.get(token);
    if (!reg) throw new Error(`Nothing registered for ${String(token)}`);

    if (reg.lifetime === Lifetime.Singleton) {
      if (!this.singletons.has(token)) this.singletons.set(token, reg.factory(this));
      return this.singletons.get(token);
    }
    return reg.factory(this);
  }

  createScope() {
    return new ScopedContainer(this);
  }
}

class ScopedContainer {
  constructor(root) {
    this.root = root;
    this.cache = new Map();
  }

  resolve(token) {
    if (!this.cache.has(token)) this.cache.set(token, this.root.resolve(token));
    return this.cache.get(token);
  }
}

// --- services ---
const DB = Symbol("Database");
const LOGGER = Symbol("Logger");
const REPO = Symbol("UserRepository");
const USERS = Symbol("UserService");

class Database {
  query() { return [{ id: 1, name: "Alice" }]; }
}
class Logger {
  info(msg) { console.log(`[info] ${msg}`); }
}
class UserRepository {
  constructor(db, logger) { this.db = db; this.logger = logger; }
  findAll() { this.logger.info("fetching users"); return this.db.query("SELECT * FROM users"); }
}
class UserService {
  constructor(repo) { this.repo = repo; }
  getUsers() { return this.repo.findAll(); }
}

// --- wiring + verification ---
const container = new Container();
container.register(DB, () => new Database(), Lifetime.Singleton);
container.register(LOGGER, () => new Logger(), Lifetime.Singleton);
container.register(REPO, (c) => new UserRepository(c.resolve(DB), c.resolve(LOGGER)));
container.register(USERS, (c) => new UserService(c.resolve(REPO)));

const service = container.resolve(USERS);
console.log("users:", service.getUsers());
console.log("singleton shared:", container.resolve(DB) === container.resolve(DB));
console.log("transient fresh:", container.resolve(REPO) !== container.resolve(REPO));

const scopeA = container.createScope();
const scopeB = container.createScope();
console.log("scoped same in scope:", scopeA.resolve(REPO) === scopeA.resolve(REPO));
console.log("scoped differs across scopes:", scopeA.resolve(REPO) !== scopeB.resolve(REPO));
console.log("singleton shared across scopes:", scopeA.resolve(DB) === scopeB.resolve(DB));
