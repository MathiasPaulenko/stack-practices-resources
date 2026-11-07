/**
 * Runnable DAO demo for the users table.
 *
 * Uses the `sqlite` package — the async wrapper around sqlite3 that exposes
 * .get()/.all()/.run(). `better-sqlite3` works too but is synchronous.
 *
 *   npm install sqlite sqlite3
 *   node dao-javascript.js
 *
 * The DAO receives an open `db` handle in its constructor — callers own the
 * connection lifecycle. In production, inject a pooled connection.
 */

import sqlite3 from 'sqlite3';
import { open } from 'sqlite';

class UserDao {
  constructor(db) {
    this.db = db;
  }

  async findById(userId) {
    const row = await this.db.get(
      'SELECT id, name, email FROM users WHERE id = ?', userId
    );
    return row || null;
  }

  async findAll() {
    return this.db.all('SELECT id, name, email FROM users');
  }

  async findPaginated(page, pageSize = 50) {
    const offset = (page - 1) * pageSize;
    return this.db.all(
      'SELECT id, name, email FROM users LIMIT ? OFFSET ?',
      pageSize, offset
    );
  }

  async save(user) {
    const result = await this.db.run(
      'INSERT INTO users (name, email) VALUES (?, ?)',
      user.name, user.email
    );
    return { id: result.lastID, name: user.name, email: user.email };
  }

  async delete(userId) {
    await this.db.run('DELETE FROM users WHERE id = ?', userId);
  }
}

// In-memory stand-in with the same interface — drop it into tests.
class FakeUserDao {
  constructor() {
    this.users = new Map();
    this.nextId = 1;
  }

  async findById(userId) {
    return this.users.get(userId) || null;
  }

  async findAll() {
    return [...this.users.values()];
  }

  async findPaginated(page, pageSize = 50) {
    const offset = (page - 1) * pageSize;
    return [...this.users.values()].slice(offset, offset + pageSize);
  }

  async save(user) {
    const saved = { ...user, id: this.nextId++ };
    this.users.set(saved.id, saved);
    return saved;
  }

  async delete(userId) {
    this.users.delete(userId);
  }
}

const db = await open({ filename: ':memory:', driver: sqlite3.Database });
await db.exec(
  'CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)'
);

const dao = new UserDao(db);
const alice = await dao.save({ name: 'Alice', email: 'alice@example.com' });
const bob = await dao.save({ name: 'Bob', email: 'bob@example.com' });

console.log('findById:', await dao.findById(alice.id));
console.log('findAll:', await dao.findAll());
console.log('paginated page 2:', await dao.findPaginated(2, 1));

await dao.delete(bob.id);
console.log('after delete:', await dao.findAll());

const fake = new FakeUserDao();
await fake.save({ name: 'Test', email: 'test@example.com' });
console.log('fake DAO:', await fake.findAll());
