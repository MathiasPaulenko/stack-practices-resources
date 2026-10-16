// Parameterized-query examples with the `pg` driver.
// Requires: npm install pg, plus a reachable Postgres instance.
// Set PG* env vars or a DATABASE_URL before running.

const { Pool } = require('pg');
const pool = new Pool({ connectionString: process.env.DATABASE_URL });

async function getUserByEmail(email) {
  // VULNERABLE — never do this:
  // const query = `SELECT * FROM users WHERE email = '${email}'`;

  // SAFE — $1 placeholders bind input as data
  const result = await pool.query(
    'SELECT * FROM users WHERE email = $1 AND active = $2',
    [email, true],
  );
  return result.rows;
}

async function searchUsers(searchTerm) {
  // LIKE wildcards in user input still need escaping
  const escapedTerm = searchTerm
    .replace(/\\/g, '\\\\')
    .replace(/%/g, '\\%')
    .replace(/_/g, '\\_');

  const result = await pool.query(
    `SELECT id, name, email FROM users
     WHERE name LIKE $1 ESCAPE '\\'
     ORDER BY name
     LIMIT 20`,
    [`%${escapedTerm}%`],
  );
  return result.rows;
}

const ALLOWED_SORT_COLUMNS = {
  name: 'name',
  email: 'email',
  created_at: 'created_at',
};

async function getUsers(sortBy = 'created_at', sortDir = 'desc', limit = 20) {
  const column = ALLOWED_SORT_COLUMNS[sortBy];
  if (!column) throw new Error(`Invalid sort column: ${sortBy}`);
  const direction = sortDir.toUpperCase() === 'ASC' ? 'ASC' : 'DESC';
  const result = await pool.query(
    `SELECT id, name, email, created_at
     FROM users WHERE active = TRUE
     ORDER BY ${column} ${direction}
     LIMIT $1`,
    [limit],
  );
  return result.rows;
}

module.exports = { getUserByEmail, searchUsers, getUsers };
