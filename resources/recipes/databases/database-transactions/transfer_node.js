// ACID transfer between accounts with node-postgres.
// Covers: BEGIN/COMMIT/ROLLBACK, atomic balance guard, deadlock retry (40P01).
// Requires: npm install pg, and DATABASE_URL pointing at PostgreSQL.

const { Pool } = require('pg');

const pool = new Pool({ connectionString: process.env.DATABASE_URL });

async function transfer(fromId, toId, amount) {
  const client = await pool.connect();
  try {
    await client.query('BEGIN');
    // Fold the balance check into the UPDATE so the guard is atomic
    const debit = await client.query(
      'UPDATE accounts SET balance = balance - $1 WHERE id = $2 AND balance >= $1 RETURNING balance',
      [amount, fromId]
    );
    if (debit.rowCount === 0) {
      throw new Error('Insufficient funds or account not found');
    }
    await client.query(
      'UPDATE accounts SET balance = balance + $1 WHERE id = $2',
      [amount, toId]
    );
    await client.query('COMMIT');
    return { success: true, newBalance: debit.rows[0].balance };
  } catch (err) {
    await client.query('ROLLBACK');
    throw err;
  } finally {
    client.release();
  }
}

async function withRetry(fn, maxRetries = 3, baseDelay = 100) {
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      return await fn();
    } catch (err) {
      if (err.code === '40P01' && attempt < maxRetries - 1) {
        const delay = baseDelay * Math.pow(2, attempt);
        console.log(`Deadlock detected, retrying in ${delay}ms...`);
        await new Promise((resolve) => setTimeout(resolve, delay));
        continue;
      }
      throw err;
    }
  }
}

async function safeTransfer(fromId, toId, amount) {
  return withRetry(() => transfer(fromId, toId, amount));
}

safeTransfer(1, 2, 100)
  .then((r) => console.log('Transfer committed:', r))
  .catch((e) => console.error('Rolled back:', e))
  .finally(() => pool.end());
