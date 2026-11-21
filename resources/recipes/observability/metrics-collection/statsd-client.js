// StatsD push-based metrics in Node.js.
// Run: npm install node-statsd && node statsd-client.js
// Requires a StatsD daemon (or a UDP sink) on localhost:8125.
const StatsD = require('node-statsd');
const client = new StatsD({ host: 'localhost', port: 8125 });

// Stand-in payment gateway so the example runs standalone.
const paymentGateway = {
  charge(amount) {
    if (amount > 400) throw new Error('declined: amount too high');
    return { id: `ch_${Date.now()}`, amount };
  },
};

function processPayment(orderId, amount) {
  const start = Date.now();

  try {
    const result = paymentGateway.charge(amount);
    client.increment('payment.success');
    client.gauge('payment.amount', amount);
    return result;
  } catch (err) {
    client.increment('payment.error', 1, ['gateway:stripe', 'error:declined']);
    throw err;
  } finally {
    client.timing('payment.duration', Date.now() - start);
  }
}

// Demo traffic so the daemon has metrics to aggregate and flush.
for (let i = 0; i < 5; i++) {
  try {
    processPayment(`order-${i}`, 50 + i * 100);
  } catch {
    // Declined payments still emit metrics — that's the point.
  }
}

setTimeout(() => client.close(), 500);
