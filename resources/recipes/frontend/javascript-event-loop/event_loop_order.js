// Execution order demo — run: node event_loop_order.js
// Shows how sync code, microtasks, and macrotasks interleave.

console.log('1. Script start');

setTimeout(() => {
  console.log('2. setTimeout (macrotask)');
}, 0);

Promise.resolve().then(() => {
  console.log('3. Promise (microtask)');
});

queueMicrotask(() => {
  console.log('4. queueMicrotask');
});

process.nextTick(() => {
  console.log('5. process.nextTick — Node only, runs before Promises');
});

console.log('6. Script end');

// Expected output:
// 1. Script start
// 6. Script end
// 5. process.nextTick
// 3. Promise (microtask)
// 4. queueMicrotask
// 2. setTimeout (macrotask)
