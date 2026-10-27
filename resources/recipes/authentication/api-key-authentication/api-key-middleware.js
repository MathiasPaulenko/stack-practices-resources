const crypto = require('crypto');

function apiKeyAuth(masterSecret) {
  return async (req, res, next) => {
    const authHeader = req.headers['x-api-key'];
    if (!authHeader) {
      return res.status(401).json({ error: 'API key required' });
    }

    // Lookup key metadata from cache or database
    const keyData = await redis.get(`apikey:${authHeader}`);
    if (!keyData) {
      return res.status(401).json({ error: 'Invalid API key' });
    }

    const key = JSON.parse(keyData);

    // Check expiration
    if (key.expires_at && new Date(key.expires_at) < new Date()) {
      return res.status(401).json({ error: 'API key expired' });
    }

    // Verify scopes for this endpoint
    const requiredScope = req.routeScope;
    if (requiredScope && !key.scopes.includes(requiredScope)) {
      return res.status(403).json({ error: 'Insufficient scope' });
    }

    // Update last used timestamp (fire and forget)
    redis.hset(`apikey:${authHeader}:meta`, 'last_used', Date.now());

    req.apiKey = key;
    next();
  };
}

// Usage
app.get('/api/v1/users', apiKeyAuth(process.env.API_SECRET), requireScope('users:read'), (req, res) => {
  res.json(users);
});
