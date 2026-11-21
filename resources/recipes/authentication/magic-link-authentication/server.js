const express = require('express');
const nodemailer = require('nodemailer');
const crypto = require('crypto');

const app = express();
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

const SECRET = process.env.APP_SECRET || 'dev-secret-change-me';
const BASE_URL = process.env.BASE_URL || 'http://localhost:3000';
const TOKEN_TTL_MS = 15 * 60 * 1000; // 15 minutes

// In-memory token store. Production: a table keyed by token_hash.
const tokens = new Map();
const sessions = new Map();

function signToken(payload) {
  const data = Buffer.from(JSON.stringify(payload)).toString('base64url');
  const sig = crypto.createHmac('sha256', SECRET).update(data).digest('base64url');
  return `${data}.${sig}`;
}

function verifyToken(token) {
  const [data, sig] = token.split('.');
  if (!data || !sig) return null;
  const expected = crypto.createHmac('sha256', SECRET).update(data).digest('base64url');
  if (!crypto.timingSafeEqual(Buffer.from(sig), Buffer.from(expected))) return null;
  return JSON.parse(Buffer.from(data, 'base64url').toString());
}

function hashToken(token) {
  return crypto.createHash('sha256').update(token).digest('hex');
}

async function getTransporter() {
  if (process.env.SMTP_HOST) {
    return nodemailer.createTransport({
      host: process.env.SMTP_HOST,
      port: Number(process.env.SMTP_PORT || 587),
      auth: { user: process.env.SMTP_USER, pass: process.env.SMTP_PASS },
    });
  }
  const testAccount = await nodemailer.createTestAccount();
  return nodemailer.createTransport({
    host: 'smtp.ethereal.email',
    port: 587,
    auth: { user: testAccount.user, pass: testAccount.pass },
  });
}

let transporterPromise = getTransporter();

// Request a magic link. Uniform response — never reveal whether the email exists.
app.post('/auth/login', async (req, res) => {
  const email = String(req.body.email || '').toLowerCase().trim();
  if (email && email.includes('@')) {
    const nonce = crypto.randomBytes(32).toString('base64url');
    const token = signToken({ email, nonce });
    const tokenHash = hashToken(token);

    // Invalidate any previous live link for this email
    for (const t of tokens.values()) {
      if (t.email === email && !t.used) t.used = true;
    }
    tokens.set(tokenHash, { email, expiresAt: Date.now() + TOKEN_TTL_MS, used: false });

    const link = `${BASE_URL}/auth/verify?token=${token}`;
    const transporter = await transporterPromise;
    const info = await transporter.sendMail({
      from: '"App" <login@auth.example.com>',
      to: email,
      subject: 'Your login link',
      text: `Log in: ${link}\n\nExpires in 15 minutes.`,
      html: `<p><a href="${link}">Log in</a> — expires in 15 minutes.</p>`,
    });
    const preview = nodemailer.getTestMessageUrl(info);
    if (preview) console.log('Magic link preview:', preview);
  }
  // Same answer either way — no account enumeration
  res.json({ message: 'If that email is registered, a login link is on its way.' });
});

// GET shows a confirm page; the token is only consumed on POST —
// email scanners that prefetch links can't burn it.
app.get('/auth/verify', (req, res) => {
  res.send(`<form method="POST" action="/auth/verify">
    <input type="hidden" name="token" value="${req.query.token || ''}">
    <button type="submit">Confirm login</button>
  </form>`);
});

app.post('/auth/verify', (req, res) => {
  const token = String(req.body.token || '');
  const payload = verifyToken(token);
  const record = payload && tokens.get(hashToken(token));

  if (!payload || !record || record.used || record.expiresAt < Date.now()) {
    return res.status(400).json({ error: 'Link invalid, expired, or already used.' });
  }
  record.used = true;

  const sessionId = crypto.randomBytes(16).toString('hex');
  sessions.set(sessionId, { email: payload.email, createdAt: Date.now() });
  res.json({ message: 'Logged in', sessionId, email: payload.email });
});

app.get('/auth/me', (req, res) => {
  const session = sessions.get(req.headers['x-session-id']);
  if (!session) return res.status(401).json({ error: 'No session' });
  res.json(session);
});

const port = Number(process.env.PORT || 3000);
app.listen(port, () => console.log(`Magic link demo on ${BASE_URL}`));
