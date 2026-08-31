const argon2 = require('argon2');

const password = 'supersecret';

async function main() {
  const start = Date.now();
  const hash = await argon2.hash(password, {
    type: argon2.argon2id,
    memoryCost: 65536,
    timeCost: 3,
    parallelism: 1
  });
  const hashMs = Date.now() - start;
  console.log(`Argon2id hash: ${hash}`);
  console.log(`hash time: ${hashMs} ms`);
  const ok = await argon2.verify(hash, password);
  console.log(`verify: ${ok}`);
}

main().catch(console.error);
