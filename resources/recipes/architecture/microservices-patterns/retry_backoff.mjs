// Retry with exponential backoff (p-retry) around a payment call.
// Companion to https://stackpractices.com/recipes/microservices-patterns/
// Usage: node retry_backoff.mjs  — or import { chargeWithRetry } in your code.

import pRetry from 'p-retry';

async function callPaymentService(orderId) {
  const response = await fetch(`https://payments.internal/api/charge/${orderId}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
  });

  if (!response.ok) {
    throw new Error(`Payment service returned ${response.status}`);
  }

  return response.json();
}

export const chargeWithRetry = async (orderId) => {
  return pRetry(() => callPaymentService(orderId), {
    retries: 5,
    factor: 2,
    minTimeout: 1000,
    maxTimeout: 30000,
    randomize: true,
    onFailedAttempt: (error) => {
      console.log(`Attempt ${error.attemptNumber} failed. ${error.retriesLeft} retries remaining.`);
    },
    retryIf: (error) => {
      // Only retry on 5xx or network errors, not 4xx
      return error.message.includes('5') || error.code === 'ECONNREFUSED';
    },
  });
};

if (process.argv[1].endsWith('retry_backoff.mjs')) {
  chargeWithRetry('ord_123')
    .then((r) => console.log(r))
    .catch((e) => {
      console.error(`All retries exhausted: ${e.message}`);
      process.exit(1);
    });
}
