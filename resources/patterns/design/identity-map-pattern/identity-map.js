/**
 * Identity Map pattern — runnable JavaScript example.
 *
 * Source: https://stackpractices.com/patterns/identity-map-pattern/
 *
 * Run: node identity-map.js
 * Expected output: true / true (same instance returned, collection queries reuse the map)
 */

class User {
  constructor(id, name, email) {
    this.id = id;
    this.name = name;
    this.email = email;
  }
}

class IdentityMap {
  constructor() {
    this.map = new Map();
  }

  get(type, key) {
    const typeMap = this.map.get(type);
    return typeMap ? typeMap.get(key) : undefined;
  }

  add(type, key, entity) {
    if (!this.map.has(type)) {
      this.map.set(type, new Map());
    }
    this.map.get(type).set(key, entity);
  }

  has(type, key) {
    const typeMap = this.map.get(type);
    return typeMap ? typeMap.has(key) : false;
  }
}

class UserMapper {
  constructor(db, identityMap) {
    this.db = db;
    this.identityMap = identityMap;
  }

  async findById(id) {
    const cached = this.identityMap.get(User, id);
    if (cached) return cached;

    const row = await this.db.get(
      "SELECT id, name, email FROM users WHERE id = ?",
      id
    );
    if (!row) return null;

    const user = new User(row.id, row.name, row.email);
    this.identityMap.add(User, id, user);
    return user;
  }

  async findAll() {
    const rows = await this.db.all("SELECT id, name, email FROM users");
    const users = [];
    for (const row of rows) {
      let user = this.identityMap.get(User, row.id);
      if (!user) {
        user = new User(row.id, row.name, row.email);
        this.identityMap.add(User, row.id, user);
      }
      users.push(user);
    }
    return users;
  }
}

// Minimal async db stand-in matching node:sqlite / sqlite-style APIs
const db = {
  rows: [{ id: 1, name: "Alice", email: "alice@example.com" }],
  async get(_sql, id) {
    return this.rows.find((r) => r.id === id) ?? null;
  },
  async all() {
    return this.rows;
  },
};

(async () => {
  const im = new IdentityMap();
  const mapper = new UserMapper(db, im);
  const u1 = await mapper.findById(1);
  const u2 = await mapper.findById(1);
  console.log(u1 === u2); // true

  const all = await mapper.findAll();
  console.log(all[0] === u1); // true — collection queries reuse the map
})();
