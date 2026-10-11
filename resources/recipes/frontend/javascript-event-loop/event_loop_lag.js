// Event loop lag monitor — run: node event_loop_lag.js
// Drift between the expected interval and the real one exposes loop pressure.

let lastCheck = performance.now();

setInterval(() => {
  const now = performance.now();
  const lag = now - lastCheck - 1000; // expected 1000ms
  if (lag > 10) {
    console.warn(`Event loop lag: ${lag.toFixed(1)}ms`);
  }
  lastCheck = now;
}, 1000);

// Simulate pressure: a synchronous burst every 2.5s.
// Watch lag spike right after each burst.
setInterval(() => {
  const end = performance.now() + 120; // 120ms blocking burst
  while (performance.now() < end) {
    Math.sqrt(Math.random());
  }
  console.log('blocking burst finished — watch the next lag report');
}, 2500);
