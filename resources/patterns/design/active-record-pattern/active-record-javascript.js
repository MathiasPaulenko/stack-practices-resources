// Active Record pattern: a User class where each instance is a table row.
// ESM required (top-level await). Expects a sqlite-compatible async driver
// exposing db.run / db.get / db.all (e.g. the `sqlite` package).

class User {
  static db = null; // Injected database connection

  constructor({ id = null, name = '', email = '' } = {}) {
    this.id = id;
    this.name = name;
    this.email = email;
  }

  async save() {
    if (this.id === null) {
      const result = await User.db.run(
        'INSERT INTO users (name, email) VALUES (?, ?)',
        this.name, this.email
      );
      this.id = result.lastID;
    } else {
      await User.db.run(
        'UPDATE users SET name = ?, email = ? WHERE id = ?',
        this.name, this.email, this.id
      );
    }
    return this;
  }

  async delete() {
    await User.db.run('DELETE FROM users WHERE id = ?', this.id);
  }

  static async findById(userId) {
    const row = await User.db.get('SELECT id, name, email FROM users WHERE id = ?', userId);
    return row ? new User(row) : null;
  }

  static async findAll() {
    const rows = await User.db.all('SELECT id, name, email FROM users');
    return rows.map(row => new User(row));
  }
}

// Usage — assign a real driver first:
// import sqlite3 from 'sqlite3';
// import { open } from 'sqlite';
// User.db = await open({ filename: 'app.db', driver: sqlite3.Database });
// await User.db.exec('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT)');
// const user = await new User({ name: 'Alice', email: 'alice@example.com' }).save();
// console.log(await User.findById(user.id));

export { User };
