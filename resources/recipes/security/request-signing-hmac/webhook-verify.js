// Webhook signature verification with nonce-based replay protection.
// Requires: npm install express redis
const crypto = require('crypto');
const express = require('express');
const redis = require('redis');

const REPLAY_WINDOW = 5 * 60; // 5 minutes
const app = express();
const redisClient = redis.createClient({ url: process.env.REDIS_URL });

async function verifyWebhook(secret, req) {
  const signature = req.headers['x-webhook-signature'];
  const timestamp = req.headers['x-webhook-timestamp'];
  const nonce = req.headers['x-webhook-nonce'];
  const body = req.body; // Buffer — needs express.raw(), not parsed JSON

  // 1. Timestamp freshness
  const now = Math.floor(Date.now() / 1000);
  if (Math.abs(now - parseInt(timestamp, 10)) > REPLAY_WINDOW) {
    throw new Error('Timestamp outside replay window');
  }

  // 2. Nonce uniqueness — SET NX is atomic, so two identical requests
  //    racing in cannot both pass
  const nonceKey = `webhook:nonce:${nonce}`;
  const created = await redisClient.set(nonceKey, '1', {
    NX: true,
    EX: REPLAY_WINDOW,
  });
  if (!created) {
    throw new Error('Nonce already used — possible replay attack');
  }

  // 3. Signature check
  const message = `${timestamp}.${nonce}.${body.toString('utf-8')}`;
  const expected = crypto
    .createHmac('sha256', secret)
    .update(message)
    .digest('base64');

  const a = Buffer.from(signature || '');
  const b = Buffer.from(expected);
  if (a.length !== b.length || !crypto.timingSafeEqual(a, b)) {
    throw new Error('Invalid signature');
  }
}

// express.raw keeps req.body as a Buffer — a JSON parser would change
// the bytes and break verification
app.post('/webhook',
  express.raw({ type: 'application/json' }),
  async (req, res) => {
    try {
      await verifyWebhook(process.env.WEBHOOK_SECRET, req);
      res.status(200).json({ ok: true });
    } catch (err) {
      res.status(401).json({ error: err.message });
    }
  },
);

async function main() {
  await redisClient.connect();
  app.listen(3000, () => console.log('webhook listener on :3000'));
}
main();
