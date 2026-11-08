// Consent management API (Express).
// Grant, withdraw, and list per-purpose consents with audit fields.

const express = require('express');
const router = express.Router();

// Grant consent for a specific purpose
router.post('/consent/:purpose', async (req, res) => {
  const { purpose } = req.params;
  const userId = req.user.id;
  const allowedPurposes = [
    'marketing', 'analytics', 'third_party', 'cookies_functional',
  ];

  if (!allowedPurposes.includes(purpose)) {
    return res.status(400).json({ error: 'Invalid consent purpose' });
  }

  const consent = await db.consents.upsert({
    user_id: userId,
    purpose,
    granted: true,
    granted_at: new Date(),
    withdrawn_at: null,
    ip_address: req.ip,
    user_agent: req.headers['user-agent'],
  });

  res.json({ purpose, granted: true, granted_at: consent.granted_at });
});

// Withdraw consent
router.delete('/consent/:purpose', async (req, res) => {
  const { purpose } = req.params;
  const userId = req.user.id;

  await db.consents.update(
    { user_id: userId, purpose, granted: true },
    { granted: false, withdrawn_at: new Date() }
  );

  // Trigger downstream: stop marketing emails, disable tracking
  await eventBus.emit('consent.withdrawn', { userId, purpose });

  res.json({ purpose, granted: false, withdrawn_at: new Date().toISOString() });
});

// Get all consents for the current user
router.get('/consents', async (req, res) => {
  const userId = req.user.id;
  const consents = await db.consents.findActive({ user_id: userId });
  res.json(consents);
});

module.exports = router;
