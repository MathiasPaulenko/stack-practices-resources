const bcrypt = require('bcrypt');

const password = 'supersecret';

async function main() {
  const start = Date.now();
  const hash = await bcrypt.hash(password, 12);
  const hashMs = Date.now() - start;
  console.log(`bcrypt hash: ${hash}`);
  console.log(`hash time: ${hashMs} ms`);
  const ok = await bcrypt.compare(password, hash);
  console.log(`verify: ${ok}`);
}

main().catch(console.error);
