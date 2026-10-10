// express_sessions.js — Express session management with Redis.
// Requires: express, express-session, connect-redis (v7+), redis (v4+)
// Start Redis locally (e.g. `docker run -p 6379:6379 redis`), then `node express_sessions.js`.
const express = require('express');
const session = require('express-session');
const { RedisStore } = require('connect-redis');
const { createClient } = require('redis');

async function main() {
  const redisClient = createClient({ url: 'redis://localhost:6379' });
  await redisClient.connect();

  const app = express();
  app.use(express.json());

  app.use(session({
    store: new RedisStore({ client: redisClient }),
    secret: process.env.SESSION_SECRET || 'dev-secret-change-me',
    resave: false,
    saveUninitialized: false,
    name: 'sessionId',
    cookie: {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'strict',
      maxAge: 3600000, // 1 hour
    },
  }));

  // Login — regenerate the session ID to prevent fixation
  app.post('/login', async (req, res) => {
    const { email, password } = req.body;
    const user = await authenticate(email, password); // your user lookup
    if (!user) return res.status(401).json({ error: 'Invalid credentials' });

    req.session.regenerate((err) => {
      if (err) return res.status(500).json({ error: 'Session error' });
      req.session.userId = user.id;
      res.json({ status: 'logged_in' });
    });
  });

  app.post('/logout', (req, res) => {
    req.session.destroy(() => res.json({ status: 'logged_out' }));
  });

  app.get('/me', (req, res) => {
    if (!req.session.userId) return res.status(401).json({ error: 'Unauthorized' });
    res.json({ userId: req.session.userId });
  });

  app.listen(3000, () => console.log('http://localhost:3000'));
}

// Stub: replace with a real user lookup (DB + bcrypt/argon2 verify).
async function authenticate(email, password) {
  return email === 'demo@example.com' && password === 'demo'
    ? { id: 'user-1' }
    : null;
}

main().catch((e) => { console.error(e); process.exit(1); });
