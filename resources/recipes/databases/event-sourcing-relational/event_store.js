/**
 * Event sourcing implementation for MySQL.
 * Requires the 'mysql2' and 'uuid' packages.
 *
 * Usage:
 *   const pool = mysql.createPool({ host: 'localhost', user: 'root', database: 'test' });
 *   const store = new EventStore(pool);
 *   await store.append('acc-1', 'Deposit', { amount: 50 });
 *   const balance = await getBalanceWithSnapshot(pool, 'acc-1');
 */

const { v4: uuidv4 } = require('uuid');

class ConcurrencyException extends Error {}

class EventStore {
  constructor(pool) {
    this.pool = pool;
  }

  async append(aggregateId, eventType, payload, expectedVersion = null) {
    const conn = await this.pool.getConnection();
    try {
      await conn.beginTransaction();

      const [rows] = await conn.execute(
        'SELECT COUNT(*) as count FROM events WHERE aggregate_id = ?',
        [aggregateId]
      );
      const currentVersion = rows[0].count;

      if (expectedVersion !== null && currentVersion !== expectedVersion) {
        throw new ConcurrencyException(
          `Expected ${expectedVersion}, found ${currentVersion}`
        );
      }

      await conn.execute(
        `INSERT INTO events (id, aggregate_id, event_type, payload, version, occurred_at)
         VALUES (?, ?, ?, ?, ?, NOW())`,
        [uuidv4(), aggregateId, eventType, JSON.stringify(payload), currentVersion + 1]
      );

      await conn.commit();
    } finally {
      conn.release();
    }
  }

  async getEvents(aggregateId, fromVersion = 0) {
    const [rows] = await this.pool.execute(
      `SELECT event_type, payload, version, occurred_at
       FROM events WHERE aggregate_id = ? AND version > ? ORDER BY version`,
      [aggregateId, fromVersion]
    );
    return rows.map(r => ({
      type: r.event_type,
      payload: JSON.parse(r.payload),
      version: r.version,
      occurredAt: r.occurred_at
    }));
  }

  async saveSnapshot(aggregateId, version, state) {
    await this.pool.execute(
      `INSERT INTO snapshots (aggregate_id, version, state, created_at)
       VALUES (?, ?, ?, NOW())`,
      [aggregateId, version, JSON.stringify(state)]
    );
  }

  async getSnapshot(aggregateId) {
    const [rows] = await this.pool.execute(
      'SELECT version, state FROM snapshots WHERE aggregate_id = ? ORDER BY version DESC LIMIT 1',
      [aggregateId]
    );
    if (rows.length === 0) return null;
    return { version: rows[0].version, state: JSON.parse(rows[0].state) };
  }
}

async function getBalanceWithSnapshot(pool, accountId) {
  const store = new EventStore(pool);
  const snapshot = await store.getSnapshot(accountId);

  let balance = 0;
  let fromVersion = 0;

  if (snapshot) {
    balance = snapshot.state.balance || 0;
    fromVersion = snapshot.version;
  }

  const events = await store.getEvents(accountId, fromVersion);

  for (const event of events) {
    if (event.type === 'Deposit') balance += event.payload.amount;
    if (event.type === 'Withdrawal') balance -= event.payload.amount;
  }

  return balance;
}

module.exports = { EventStore, ConcurrencyException, getBalanceWithSnapshot };
