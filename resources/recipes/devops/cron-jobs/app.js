// In-app scheduling with node-cron.
// Install: npm install   (see package.json)
// Run:     node app.js
const cron = require('node-cron');

// Every 15 minutes
cron.schedule('*/15 * * * *', () => {
  console.log(`[${new Date().toISOString()}] Running every 15 minutes`);
});

// Every day at 3:00 AM
cron.schedule('0 3 * * *', () => {
  console.log(`[${new Date().toISOString()}] Running daily backup`);
});

// Every Monday at 9:00 AM
cron.schedule('0 9 * * 1', () => {
  console.log(`[${new Date().toISOString()}] Running weekly report`);
});

// Optional: pin a job to a timezone instead of host local time
cron.schedule('0 3 * * *', () => {
  console.log('Daily backup in America/New_York time');
}, { timezone: 'America/New_York' });

console.log('Scheduler started — Ctrl+C to stop');
