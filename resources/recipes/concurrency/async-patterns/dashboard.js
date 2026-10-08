// Async fan-out with Promise.all vs Promise.allSettled — runnable demo.
// Simulates three I/O calls with fake latency; no network needed.
// Run: node dashboard.js

const delay = (ms, value) => new Promise((resolve) => setTimeout(() => resolve(value), ms));

const getProfile = (userId) => delay(120, { id: userId, name: `user-${userId}` });
const getOrders = (userId) => delay(200, [`order-1-${userId}`, `order-2-${userId}`]);
const getRecommendations = (userId, { fail = false } = {}) =>
  fail
    ? delay(80).then(() => {
        throw new Error('recommendations service returned 503');
      })
    : delay(150, [`item-${userId}-a`, `item-${userId}-b`]);

// Fails fast: one rejection rejects the whole Promise.all.
async function fetchUserDashboard(userId) {
  const [profile, orders, recommendations] = await Promise.all([
    getProfile(userId),
    getOrders(userId),
    getRecommendations(userId, { fail: true }),
  ]);
  return { profile, orders, recommendations };
}

// Resilient: every outcome is reported, failures become fallbacks.
async function fetchDashboardResilient(userId) {
  const [profile, orders, recommendations] = await Promise.allSettled([
    getProfile(userId),
    getOrders(userId),
    getRecommendations(userId, { fail: true }),
  ]);

  return {
    profile: profile.status === 'fulfilled' ? profile.value : null,
    orders: orders.status === 'fulfilled' ? orders.value : [],
    recommendations: recommendations.status === 'fulfilled' ? recommendations.value : [],
  };
}

async function main() {
  try {
    await fetchUserDashboard(42);
  } catch (err) {
    console.log('Promise.all rejected:', err.message);
  }

  const resilient = await fetchDashboardResilient(42);
  console.log('Promise.allSettled result:', JSON.stringify(resilient));
}

main();
