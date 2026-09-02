FROM node:20-alpine

WORKDIR /app

# Minimal API stub — in a real project, copy your source and install deps
RUN npm init -y && npm install express pg

COPY <<'EOF' /app/index.js
const express = require('express');
const { Pool } = require('pg');
const app = express();
const port = 3000;

const pool = new Pool({
  connectionString: process.env.DATABASE_URL || 'postgres://appuser:apppass@db:5432/appdb'
});

app.get('/', async (req, res) => {
  try {
    const result = await pool.query('SELECT NOW() as now');
    res.json({ status: 'ok', db_time: result.rows[0].now });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.get('/health', (req, res) => {
  res.json({ status: 'healthy' });
});

app.listen(port, () => {
  console.log(`API running on port ${port}`);
});
EOF

EXPOSE 3000
CMD ["node", "index.js"]
