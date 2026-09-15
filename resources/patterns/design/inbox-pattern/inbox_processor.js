// Inbox Pattern implementation with SQLite for idempotent event processing.

const crypto = require('crypto');

class InboxProcessor {
  constructor(db) {
    this.db = db;
    this.MAX_RETRIES = 3;
  }

  async init() {
    await this.db.exec(`
      CREATE TABLE IF NOT EXISTS inbox (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        message_id TEXT UNIQUE NOT NULL,
        payload TEXT NOT NULL,
        status TEXT DEFAULT 'pending',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        processed_at DATETIME,
        retry_count INTEGER DEFAULT 0
      )
    `);
    await this.db.exec('CREATE INDEX IF NOT EXISTS idx_status ON inbox(status)');
  }

  generateMessageId(payload) {
    const content = JSON.stringify(payload, Object.keys(payload).sort());
    return crypto.createHash('sha256').update(content).digest('hex').substring(0, 16);
  }

  async receive(payload) {
    const messageId = this.generateMessageId(payload);
    const payloadJson = JSON.stringify(payload);
    try {
      await this.db.run(
        'INSERT INTO inbox (message_id, payload) VALUES (?, ?)',
        [messageId, payloadJson]
      );
      return true;
    } catch (err) {
      if (err.message.includes('UNIQUE constraint failed')) {
        return false; // Duplicate
      }
      throw err;
    }
  }

  async processPending(processorFunc) {
    const rows = await this.db.all(
      "SELECT id, message_id, payload, retry_count FROM inbox WHERE status = 'pending'"
    );

    for (const row of rows) {
      await this.db.run("UPDATE inbox SET status = 'processing' WHERE id = ?", [row.id]);
      try {
        const payload = JSON.parse(row.payload);
        const result = await processorFunc(payload);
        await this.db.run(
          "UPDATE inbox SET status = 'completed', processed_at = CURRENT_TIMESTAMP WHERE id = ?",
          [row.id]
        );
        console.log(`Processed ${row.message_id}: ${result}`);
      } catch (err) {
        const newRetries = row.retry_count + 1;
        const status = newRetries >= this.MAX_RETRIES ? 'failed' : 'pending';
        await this.db.run(
          'UPDATE inbox SET status = ?, retry_count = ? WHERE id = ?',
          [status, newRetries, row.id]
        );
        console.log(`Failed ${row.message_id} (retry ${newRetries}): ${err.message}`);
      }
    }
  }

  async getStats() {
    const rows = await this.db.all('SELECT status, COUNT(*) as count FROM inbox GROUP BY status');
    return Object.fromEntries(rows.map(r => [r.status, r.count]));
  }
}

module.exports = { InboxProcessor };
