const functions = require('@google-cloud/functions-framework');

// Cloud Scheduler invokes the function over HTTP with an OIDC token.
// Register an HTTP handler — a cloudEvent handler won't fire.
async function cleanupExpiredRecords() {
  // Replace with your cleanup logic (e.g. delete stale Firestore docs).
  console.log('cleanupExpiredRecords: nothing to clean in the example');
}

functions.http('scheduledCleanup', async (req, res) => {
  console.log('Running scheduled cleanup at:', new Date().toISOString());
  await cleanupExpiredRecords();
  res.status(204).send();
});
