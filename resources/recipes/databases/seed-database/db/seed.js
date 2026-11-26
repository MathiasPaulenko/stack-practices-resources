import { Client } from 'pg';
import { readdirSync, readFileSync } from 'fs';
import { join } from 'path';

async function seed() {
  if (process.env.NODE_ENV === 'production') {
    console.error('Refusing to seed production database');
    process.exit(1);
  }
  const client = new Client({ connectionString: process.env.DATABASE_URL });
  await client.connect();

  const seedsDir = './db/seeds';
  const files = readdirSync(seedsDir).filter(f => f.endsWith('.sql')).sort();

  await client.query('BEGIN');
  try {
    for (const file of files) {
      console.log(`Running: ${file}`);
      await client.query(readFileSync(join(seedsDir, file), 'utf8'));
    }
    await client.query('COMMIT');
    console.log('Seeding complete');
  } catch (err) {
    await client.query('ROLLBACK');
    throw err;
  } finally {
    await client.end();
  }
}

seed().catch(err => { console.error(err); process.exit(1); });
