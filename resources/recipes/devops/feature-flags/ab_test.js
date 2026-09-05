// A/B test variant assignment with deterministic bucketing.

import { createHash } from "crypto";

function hashBucket(userId, flag) {
  const hash = createHash("md5").update(`${flag}:${userId}`).digest("hex");
  return parseInt(hash.slice(0, 8), 16) % 100;
}

function getVariant(flag, userId) {
  const bucket = hashBucket(userId, flag);
  return bucket < 50 ? "A" : "B";
}

// Simulate an A/B test over 1000 users
const results = { A: 0, B: 0 };
for (let i = 0; i < 1000; i++) {
  const variant = getVariant("checkout_redesign", `user_${i}`);
  results[variant]++;
}

console.log("A/B test distribution (1000 users):");
console.log(`  Variant A: ${results.A} users`);
console.log(`  Variant B: ${results.B} users`);

// Example analytics event
const userId = "user_456";
const variant = getVariant("checkout_redesign", userId);
console.log(`\nUser ${userId} -> variant ${variant}`);
console.log('analytics.track({ experiment: "checkout_redesign", userId, variant, event: "checkout_view" });');

export { getVariant, hashBucket };
