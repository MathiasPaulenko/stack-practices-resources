// Optimistic locking example with PostgreSQL and Node.js.
//
// Run: npm install pg
// Set: DATABASE_URL or PG* env vars

const { Pool } = require('pg');

const pool = new Pool({
  // Use env vars or pass connection config
});

async function updateProductPrice(productId, newPrice, expectedVersion) {
  const result = await pool.query(
    `UPDATE products
     SET price = $1, version = version + 1, updated_at = NOW()
     WHERE id = $2 AND version = $3
     RETURNING id, version;`,
    [newPrice, productId, expectedVersion]
  );

  if (result.rowCount === 0) {
    const current = await pool.query(
      'SELECT version FROM products WHERE id = $1',
      [productId]
    );
    throw new Error(
      `Version conflict: expected ${expectedVersion}, found ${current.rows[0]?.version}. Please retry.`
    );
  }

  return result.rows[0];
}

async function withRetry(fn, maxRetries = 3, baseDelay = 50) {
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      return await fn();
    } catch (err) {
      if (!err.message.includes('Version conflict') || attempt === maxRetries - 1) {
        throw err;
      }
      const delay = baseDelay * (2 ** attempt) + Math.random() * 50;
      await new Promise((r) => setTimeout(r, delay));
    }
  }
}

// Express route
const express = require('express');
const app = express();
app.use(express.json());

app.put('/products/:id', async (req, res) => {
  try {
    const product = await updateProductPrice(
      req.params.id,
      req.body.price,
      req.body.version
    );
    res.json(product);
  } catch (err) {
    res.status(409).json({ error: err.message });
  }
});

if (require.main === module) {
  app.listen(3000, () => console.log('Listening on :3000'));
}
