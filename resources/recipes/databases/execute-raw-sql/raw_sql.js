// Safe raw SQL with node:sqlite (Node 22+, zero deps). Same patterns apply to pg with $1.
import { DatabaseSync } from 'node:sqlite';

const db = new DatabaseSync(':memory:');

db.exec('CREATE TABLE users (id INTEGER PRIMARY KEY, email TEXT, role TEXT, active INTEGER)');

// Parameterized insert — never interpolate values
db.prepare('INSERT INTO users (email, role, active) VALUES (?, ?, ?)')
    .run('alice@example.com', 'admin', 1);

// Bulk insert in a transaction
const insert = db.prepare('INSERT INTO users (email, role, active) VALUES (?, ?, ?)');
db.exec('BEGIN');
for (const row of [['bob@example.com', 'user', 1], ['carol@example.com', 'user', 0]]) {
    insert.run(...row);
}
db.exec('COMMIT');

// Parameterized SELECT
const found = db.prepare('SELECT id, email FROM users WHERE email = ? AND active = ?')
    .get('alice@example.com', 1);
console.log('found:', found);

// Dynamic IN clause — expand placeholders to match the list
const emails = ['alice@example.com', 'bob@example.com'];
const placeholders = emails.map(() => '?').join(',');
const rows = db.prepare(`SELECT email FROM users WHERE email IN (${placeholders})`)
    .all(...emails);
console.log('in-clause:', rows.map((r) => r.email));

// Dynamic identifier — whitelist, then interpolate the validated name
const ALLOWED_COLUMNS = new Set(['id', 'email', 'role', 'active']);
const column = 'role';
if (!ALLOWED_COLUMNS.has(column)) {
    throw new Error(`Invalid column: ${column}`);
}
const grouped = db.prepare(`SELECT ${column}, COUNT(*) AS n FROM users GROUP BY ${column}`).all();
console.log('whitelist:', grouped);

db.close();
