// Stripe-style webhook signature verification — runnable demo (node:crypto only).
// Simulates a signed delivery and verifies it, including the attack cases:
// forged signature, stale timestamp, and tampered payload.
//
// Run: node stripe-verifier.js

const crypto = require("crypto");

const SECRET = "whsec_demo_secret";
const TOLERANCE_SECONDS = 300;

// ---------- Producer side ----------

function signDelivery(rawBody) {
  const timestamp = Math.floor(Date.now() / 1000);
  const signedPayload = `${timestamp}.${rawBody}`;
  const sig = crypto.createHmac("sha256", SECRET).update(signedPayload).digest("hex");
  return { timestamp, header: `t=${timestamp},v1=${sig}` };
}

// ---------- Consumer side ----------

function verifyStripeSignature(rawBody, signatureHeader) {
  const parts = Object.fromEntries(
    signatureHeader.split(",").map((e) => e.split("="))
  );
  const { t: timestamp, v1: sig } = parts;
  if (!timestamp || !sig) throw new Error("Malformed signature header");

  if (Math.abs(Date.now() / 1000 - Number(timestamp)) > TOLERANCE_SECONDS) {
    throw new Error("Timestamp out of tolerance");
  }

  const signedPayload = `${timestamp}.${rawBody}`;
  const expected = crypto
    .createHmac("sha256", SECRET)
    .update(signedPayload)
    .digest("hex");

  const a = Buffer.from(sig);
  const b = Buffer.from(expected);
  if (a.length !== b.length || !crypto.timingSafeEqual(a, b)) {
    throw new Error("Invalid signature");
  }
  return true;
}

// ---------- Demo ----------

const rawBody = JSON.stringify({ type: "payment_intent.succeeded", amount: 4900 });
const { header } = signDelivery(rawBody);

const cases = [
  ["legitimate delivery", rawBody, header],
  ["replayed signature on tampered payload", rawBody.replace("4900", "49"), header],
  ["forged signature", rawBody, `t=${Math.floor(Date.now() / 1000)},v1=${"0".repeat(64)}`],
  ["stale timestamp", rawBody, `t=${Math.floor(Date.now() / 1000) - 3600},v1=abc`],
];

for (const [label, body, sigHeader] of cases) {
  try {
    verifyStripeSignature(body, sigHeader);
    console.log(`${label}: ACCEPTED`);
  } catch (err) {
    console.log(`${label}: REJECTED (${err.message})`);
  }
}
