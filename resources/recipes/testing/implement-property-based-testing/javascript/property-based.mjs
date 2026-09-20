// Property-based testing examples with fast-check.
// Run with: npm install && npm test
import fc from 'fast-check';

// Spread preserves surrogate pairs; s.split('').reverse() would fail this
// property on astral characters — exactly the kind of edge case PBT finds.
function reverse(s) {
  return [...s].reverse().join('');
}

// Property: reverse(reverse(s)) === s
fc.assert(
  fc.property(fc.string(), (s) => {
    return reverse(reverse(s)) === s;
  }),
  { numRuns: 1000 }
);

// Property: sorting keeps the length and produces a monotonic list
fc.assert(
  fc.property(fc.array(fc.integer()), (arr) => {
    const sorted = arr.slice().sort((a, b) => a - b);
    for (let i = 1; i < sorted.length; i++) {
      if (sorted[i - 1] > sorted[i]) return false;
    }
    return sorted.length === arr.length;
  })
);

// Model-based testing: commands implement check() and run()
class ListModel {
  constructor() { this.items = []; }
  push(x) { this.items.push(x); }
  pop() { return this.items.pop(); }
  get length() { return this.items.length; }
}

// System under test — swap for your own implementation
class MyList {
  constructor() { this.items = []; }
  push(x) { this.items.push(x); }
  pop() { return this.items.pop(); }
}

class PushCommand {
  constructor(value) { this.value = value; }
  check() { return true; }
  run(model, real) {
    model.push(this.value);
    real.push(this.value);
  }
}

class PopCommand {
  check(model) { return model.length > 0; }
  run(model, real) {
    if (real.pop() !== model.pop()) {
      throw new Error('pop mismatch between model and implementation');
    }
  }
}

fc.assert(
  fc.property(
    fc.commands([
      fc.integer().map((n) => new PushCommand(n)),
      fc.constant(new PopCommand()),
    ]),
    (cmds) => {
      fc.modelRun(() => ({ model: new ListModel(), real: new MyList() }), cmds);
    }
  )
);

console.log('All property-based checks passed.');
