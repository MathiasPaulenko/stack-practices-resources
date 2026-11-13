// Argon2id password hashing demo — hash, verify, and rehash-on-upgrade.
// Companion to https://stackpractices.com/recipes/hash-passwords-argon2/
// Run: npm install && npm run argon2

import argon2 from 'argon2';

const OPTIONS = {
    type: argon2.argon2id,
    memoryCost: 65536,   // 64 MiB — RFC 9106 profile
    timeCost: 3,
    parallelism: 4,
    hashLength: 32,
    saltLength: 16
};

async function hashPassword(password) {
    return argon2.hash(password, OPTIONS);
}

async function verifyPassword(password, hash) {
    try {
        return await argon2.verify(hash, password);
    } catch {
        return false;
    }
}

async function verifyAndRehash(password, hash) {
    const valid = await verifyPassword(password, hash);
    if (!valid) return { valid: false, newHash: null };
    const newHash = argon2.needsRehash(hash, OPTIONS)
        ? await hashPassword(password)
        : null;
    return { valid: true, newHash };
}

const password = 'correct horse battery staple';
const start = performance.now();
const hashed = await hashPassword(password);
const elapsed = (performance.now() - start).toFixed(0);

console.log(`Hash:    ${hashed}`);
console.log(`Time:    ${elapsed} ms (target: 250–500 ms on your hardware)`);
console.log(`Valid:   ${await verifyPassword(password, hashed)}`);
console.log(`Invalid: ${await verifyPassword('wrong', hashed)}`);

const { newHash } = await verifyAndRehash(password, hashed);
console.log(`Rehash needed: ${newHash !== null}`);
