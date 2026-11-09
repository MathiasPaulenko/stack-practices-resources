// Express middleware that adds RFC 9745 `Deprecation` and RFC 8594 `Sunset`
// headers to every response on a deprecated route version.
//
// `Deprecation` marks the resource as deprecated (boolean or HTTP-date).
// `Sunset`  announces when it will stop responding (HTTP-date).
//
// Usage:
//   const { deprecationHeaders } = require('./express-deprecation-headers');
//   app.use('/v1', deprecationHeaders({
//     sunsetAt: new Date('2027-10-15T00:00:00Z'),
//     migrationUrl: 'https://docs.example.com/migrate/v1-to-v2',
//   }));

function deprecationHeaders({ sunsetAt, migrationUrl }) {
  const sunsetHttpDate = sunsetAt.toUTCString(); // RFC 8594 wants an HTTP-date

  return (req, res, next) => {
    res.set('Deprecation', 'true');          // RFC 9745 — or an @-unix-timestamp
    res.set('Sunset', sunsetHttpDate);       // RFC 8594
    if (migrationUrl) {
      // Link header lets tooling discover the migration guide automatically.
      res.append('Link', `<${migrationUrl}>; rel="deprecation"`);
    }
    next();
  };
}

// After the cutoff date the route should stop serving entirely and answer
// 410 Gone with a pointer to the migration guide.
function goneHandler(migrationUrl) {
  return (req, res) => {
    res.status(410).json({
      error: 'gone',
      message: 'This API version was shut down. See the migration guide.',
      migration_url: migrationUrl,
    });
  };
}

module.exports = { deprecationHeaders, goneHandler };
