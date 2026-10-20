// ES Module — private state via non-exported declarations
// Run: node esm-main.js (needs "type": "module" or .mjs)

let count = 0; // Module-scoped — not exported, not accessible

function log(operation) {
  console.log(`Counter ${operation}: ${count}`);
}

export function increment() {
  count++;
  log('incremented');
  return count;
}

export function decrement() {
  count--;
  log('decremented');
  return count;
}

export function getCount() {
  return count;
}
