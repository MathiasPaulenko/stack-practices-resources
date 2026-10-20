// IIFE Module Pattern — private state via closure (pre-ES6 style)
// Run: node iife-counter.js

const CounterModule = (function () {
  let count = 0; // Private state — unreachable from outside

  function log(operation) {
    console.log(`Counter ${operation}: ${count}`);
  }

  return {
    increment() {
      count++;
      log('incremented');
      return count;
    },
    decrement() {
      count--;
      log('decremented');
      return count;
    },
    getCount() {
      return count;
    },
  };
})();

CounterModule.increment();
CounterModule.increment();
console.log(CounterModule.getCount()); // 2
console.log(CounterModule.count); // undefined — private
