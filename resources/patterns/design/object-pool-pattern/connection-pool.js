// Object Pool pattern — JavaScript implementation.
// Fixed-size pool; acquire() fails fast when empty. Always release()
// in a finally block so objects return to the pool.

class DatabaseConnection {
  static #counter = 0;

  constructor() {
    this.id = ++DatabaseConnection.#counter;
    this.active = false;
    console.log(`Created connection ${this.id} (expensive)`);
  }

  open() { this.active = true; return this; }
  close() { this.active = false; }

  query(sql) {
    if (!this.active) throw new Error('Not open');
    return `Result for: ${sql}`;
  }
}

class PoolExhaustedError extends Error {}

class ConnectionPool {
  constructor(maxSize = 5) {
    this.maxSize = maxSize;
    this.available = [];
    this.inUse = new Set();

    for (let i = 0; i < maxSize; i++) {
      this.available.push(new DatabaseConnection());
    }
  }

  acquire() {
    if (this.available.length === 0) {
      throw new PoolExhaustedError(
        `No free objects — pool size ${this.maxSize}`
      );
    }
    const conn = this.available.pop();
    this.inUse.add(conn);
    return conn.open();
  }

  release(conn) {
    conn.close();
    this.inUse.delete(conn);
    this.available.push(conn);
  }

  // Convenience wrapper: fn always gets a released object back
  async withConnection(fn) {
    const conn = this.acquire();
    try {
      return await fn(conn);
    } finally {
      this.release(conn);
    }
  }
}

// Demo
const pool = new ConnectionPool(3);

const conn = pool.acquire();
try {
  console.log(conn.query('SELECT * FROM users'));
} finally {
  pool.release(conn);
}

// Reuses the same object — no new "(expensive)" line
const conn2 = pool.acquire();
try {
  console.log(conn2.query('SELECT * FROM orders'));
} finally {
  pool.release(conn2);
}
