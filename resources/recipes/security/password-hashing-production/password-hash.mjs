// Argon2id hashing with pepper and needsRehash upgrade (requires: npm install argon2)
import argon2 from 'argon2';

const PEPPER = process.env.PASSWORD_PEPPER ?? 'local-dev-pepper';
const OPTIONS = {
  type: argon2.argon2id,
  timeCost: 3,
  memoryCost: 65536,
  parallelism: 4,
};

export async function hashPassword(password) {
  return argon2.hash(password + PEPPER, OPTIONS);
}

export async function verifyAndMaybeUpgrade(password, storedHash) {
  try {
    const valid = await argon2.verify(storedHash, password + PEPPER);
    if (!valid) return { valid: false, newHash: null };
    if (argon2.needsRehash(storedHash, OPTIONS)) {
      return { valid: true, newHash: await hashPassword(password) };
    }
    return { valid: true, newHash: null };
  } catch {
    return { valid: false, newHash: null };
  }
}
