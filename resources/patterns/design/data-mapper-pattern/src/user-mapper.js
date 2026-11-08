/**
 * Data Mapper pattern over Node.js built-in SQLite.
 *
 * Run:  node user-mapper.js   (Node 22.5+; pass --experimental-sqlite on Node 22)
 */
class User {
  constructor(name, email) {
    this.id = null;
    this.name = name;
    this.email = email;
  }

  updateEmail(newEmail) {
    if (!newEmail.includes('@')) throw new Error('Invalid email');
    this.email = newEmail;
  }
}

class UserMapper {
  constructor(db) {
    this.db = db;
  }

  findById(id) {
    const row = this.db
      .prepare('SELECT id, name, email FROM users WHERE id = ?')
      .get(id);
    if (!row) return null;
    const user = new User(row.name, row.email);
    user.id = row.id;
    return user;
  }

  findAll() {
    return this.db
      .prepare('SELECT id, name, email FROM users')
      .all()
      .map(row => {
        const user = new User(row.name, row.email);
        user.id = row.id;
        return user;
      });
  }

  insert(user) {
    const result = this.db
      .prepare('INSERT INTO users (name, email) VALUES (?, ?)')
      .run(user.name, user.email);
    user.id = result.lastInsertRowid;
  }

  update(user) {
    this.db
      .prepare('UPDATE users SET name = ?, email = ? WHERE id = ?')
      .run(user.name, user.email, user.id);
  }

  delete(id) {
    this.db.prepare('DELETE FROM users WHERE id = ?').run(id);
  }
}

const { DatabaseSync } = require('node:sqlite');
const db = new DatabaseSync(':memory:');
db.exec('CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)');

const mapper = new UserMapper(db);
const user = new User('Alice', 'alice@example.com');
mapper.insert(user);
console.log(`Inserted user with ID: ${user.id}`);

const loaded = mapper.findById(user.id);
console.log(loaded.name, loaded.email);
