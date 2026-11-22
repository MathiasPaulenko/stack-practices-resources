// Synchronous REST call with a 5s timeout via AbortController.
// Companion to https://stackpractices.com/recipes/microservices-communication/
// Usage: node rest_client.mjs [orderId]

export async function getOrder(orderId) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 5000);
  const res = await fetch(`http://orders-service/orders/${orderId}`, {
    signal: controller.signal,
  });
  clearTimeout(timeout);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

if (process.argv[1].endsWith('rest_client.mjs')) {
  const orderId = process.argv[2] || 'ord_123';
  getOrder(orderId)
    .then((order) => console.log(JSON.stringify(order, null, 2)))
    .catch((err) => {
      console.error(`orders-service unreachable: ${err.message}`);
      process.exit(1);
    });
}
