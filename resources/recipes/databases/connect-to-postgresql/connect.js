// Connect to PostgreSQL with node-pg: pool, parameterized query, transaction.
// npm install pg
const { Pool } = require('pg');

const pool = new Pool({
    host: process.env.PGHOST || 'localhost',
    database: process.env.PGDATABASE || 'mydb',
    user: process.env.PGUSER || 'user',
    password: process.env.PGPASSWORD || 'pass',
    // Local dev needs no SSL; in production use ssl: { rejectUnauthorized: true }
    // and point PGSSLROOTCERT at your CA cert. Never disable verification.
    ssl: false,
    max: 20,
    idleTimeoutMillis: 30000,
    connectionTimeoutMillis: 5000
});

async function getUser(id) {
    const result = await pool.query('SELECT * FROM users WHERE id = $1', [id]);
    return result.rows[0];
}

async function transferBalance(fromId, toId, amount) {
    const client = await pool.connect();
    try {
        await client.query('BEGIN');
        await client.query(
            'UPDATE accounts SET balance = balance - $1 WHERE id = $2',
            [amount, fromId]
        );
        await client.query(
            'UPDATE accounts SET balance = balance + $1 WHERE id = $2',
            [amount, toId]
        );
        await client.query('COMMIT');
    } catch (err) {
        await client.query('ROLLBACK');
        throw err;
    } finally {
        client.release();
    }
}

async function main() {
    const user = await getUser(1);
    console.log(user);
    await transferBalance(1, 2, 10);
    await pool.end();
}

main().catch(async (err) => {
    console.error(err);
    await pool.end();
    process.exit(1);
});
