const express = require('express');
const app = express();

function problemResponse(type, title, detail, status, instance) {
  const body = { type, title, detail, status };
  if (instance) body.instance = instance;
  return body;
}

app.get('/users/:userId', (req, res, next) => {
  const userId = parseInt(req.params.userId, 10);
  if (Number.isNaN(userId) || userId <= 0) {
    return res.status(404)
      .set('Content-Type', 'application/problem+json')
      .json(problemResponse(
        'https://api.example.com/errors/not-found',
        'User Not Found',
        `No user with id ${req.params.userId}`,
        404,
        req.originalUrl
      ));
  }
  res.json({ id: userId, name: 'Ada' });
});

app.get('/crash', (req, res, next) => {
  next(new Error('Intentional crash for testing'));
});

// Global error handler (must be last)
app.use((err, req, res, next) => {
  console.error(err);
  const status = err.status || 500;
  res.status(status)
    .set('Content-Type', 'application/problem+json')
    .json(problemResponse(
      'https://api.example.com/errors/server-error',
      'Internal Server Error',
      process.env.NODE_ENV === 'production' ? 'Something went wrong.' : err.message,
      status,
      req.originalUrl
    ));
});

if (require.main === module) {
  app.listen(3000, () => console.log('Server running on port 3000'));
}

module.exports = app;
