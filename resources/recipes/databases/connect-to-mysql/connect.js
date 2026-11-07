// Connect to MySQL with mysql2: pool, parameterized query, transaction.
// npm install mysql2
const mysql = require('mysql2/promise');

const pool = mysql.createPool({
    host: process.env.DB_HOST || 'localhost',
    database: process.env.DB_NAME || 'mydb',
    user: process.env.DB_USER || 'user',
    password: process.env.DB_PASSWORD || 'pass',
    // Local dev needs no SSL; in production use ssl: { ca: <CA bundle> }.
    connectionLimit: 10,
    waitForConnections: true,
    queueLimit: 0,
    connectTimeout: 10000,
    enableKeepAlive: true,
    keepAliveInitialDelay: 10000
});

async function getUser(id) {
    const [rows] = await pool.execute('SELECT * FROM users WHERE id = ?', [id]);
    return rows[0];
}

async function transferBalance(fromId, toId, amount) {
    const conn = await pool.getConnection();
    try {
        await conn.beginTransaction();
        await conn.execute(
            'UPDATE accounts SET balance = balance - ? WHERE id = ?',
            [amount, fromId]
        );
        await conn.execute(
            'UPDATE accounts SET balance = balance + ? WHERE id = ?',
            [amount, toId]
        );
        await conn.commit();
    } catch (err) {
        await conn.rollback();
        throw err;
    } finally {
        conn.release();
    }
}

(async () => {
    console.log(await getUser(1));
    await transferBalance(1, 2, 25.0);
    const [rows] = await pool.query('SELECT * FROM accounts');
    console.log(rows);
    await pool.end();
})().catch(err => {
    console.error(err);
    process.exit(1);
});
