// Database deadlock retry example with Knex.js and MySQL
const knex = require('knex')({ client: 'mysql2' });

async function withDeadlockRetry(fn, maxRetries = 3) {
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      return await fn();
    } catch (err) {
      if (err.code !== 'ER_LOCK_DEADLOCK' || attempt === maxRetries - 1) {
        throw err;
      }
      const delay = 100 * (2 ** attempt) + Math.random() * 20;
      await new Promise(r => setTimeout(r, delay));
    }
  }
}

async function transferFunds(fromId, toId, amount) {
  return withDeadlockRetry(async () => {
    await knex.transaction(async (trx) => {
      const ids = [fromId, toId].sort((a, b) => a - b);
      await trx('accounts').whereIn('id', ids).forUpdate();

      await trx('accounts').where('id', fromId).decrement('balance', amount);
      await trx('accounts').where('id', toId).increment('balance', amount);
    });
  });
}

// Usage
(async () => {
  await transferFunds(1, 2, 100);
  console.log('Transfer completed');
})();
