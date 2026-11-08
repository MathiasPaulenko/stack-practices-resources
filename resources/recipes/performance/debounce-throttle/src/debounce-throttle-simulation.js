/**
 * Event burst simulation: debounce vs throttle over a synthetic stream.
 * Run: node src/debounce-throttle-simulation.js
 */

const DEBOUNCE_WAIT = 250; // ms
const THROTTLE_LIMIT = 300; // ms

function simulate(events) {
  let throttleLast = -Infinity;
  let throttleFires = 0;
  let quietStart = null;
  let debounceFires = 0;

  for (const t of events) {
    if (t - throttleLast >= THROTTLE_LIMIT) {
      throttleLast = t;
      throttleFires++;
    }
    // Debounce: a quiet gap >= wait since the last event closes a burst.
    if (quietStart !== null && t - quietStart >= DEBOUNCE_WAIT) {
      debounceFires++;
    }
    quietStart = t;
  }
  if (quietStart !== null) debounceFires++;

  console.log(
    `events=${events.length}  raw=${events.length}  ` +
      `debounce=${debounceFires}  throttle=${throttleFires}`
  );
}

const burst = Array.from({ length: 12 }, (_, i) => i * 25);
const tail = [1000, 1050, 1100];
simulate(burst.concat(tail));
