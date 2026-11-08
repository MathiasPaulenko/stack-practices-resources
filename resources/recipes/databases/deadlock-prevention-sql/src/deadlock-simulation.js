/**
 * Deadlock simulation: unordered vs ordered lock acquisition.
 * Models a wait-for graph — no threads needed, deterministic output.
 */

class LockManager {
  constructor() {
    this.held = new Map(); // row -> transaction id
  }

  // A transaction requests rows in order; returns 'deadlock' if a
  // circular wait would form, 'ok' when all locks are acquired.
  transfer(txnId, rows) {
    const acquired = [];
    for (const row of rows) {
      const holder = this.held.get(row);
      if (holder && holder !== txnId) {
        const holderWants = this.waitingOn?.get(holder);
        if (holderWants && this.held.get(holderWants) === txnId) {
          return "deadlock";
        }
      }
      acquired.push(row);
    }
    acquired.forEach((r) => this.held.set(r, txnId));
    return "ok";
  }

  releaseAll(txnId) {
    for (const [row, holder] of this.held) {
      if (holder === txnId) this.held.delete(row);
    }
  }
}

function simulateUnordered() {
  // T1 holds A, wants B. T2 holds B, wants A.
  const lm = new LockManager();
  lm.held.set("A", "T1");
  lm.held.set("B", "T2");
  lm.waitingOn = new Map([["T1", "B"], ["T2", "A"]]);
  const t1 = lm.transfer("T1", ["B"]); // waits for B (held by T2, which waits on A held by T1)
  const t2 = lm.transfer("T2", ["A"]);
  return [t1, t2];
}

function simulateOrdered() {
  // Both transactions lock A first, then B — no cycle possible.
  const lm = new LockManager();
  const t1 = lm.transfer("T1", ["A", "B"]);
  lm.releaseAll("T1");
  const t2 = lm.transfer("T2", ["A", "B"]); // same sorted order
  lm.releaseAll("T2");
  return [t1, t2];
}

function executeWithRetry(fn, maxRetries = 3) {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    const result = fn();
    if (!result.includes("deadlock")) return result;
    // Exponential backoff + jitter keeps retried txns from colliding again.
    // (delay is illustrative in this synchronous simulation)
    void (Math.pow(2, attempt) * 10 + Math.random() * 10);
  }
  return ["failed: max retries exceeded"];
}

console.log("=== Unordered lock acquisition ===");
console.log(simulateUnordered());
console.log("\n=== Ordered lock acquisition ===");
console.log(simulateOrdered());
console.log("\n=== Retry with jitter ===");
console.log(executeWithRetry(simulateOrdered));
