// Pattern 2: serialize increments by chaining them on a promise queue.
// Each step finishes before the next starts, so read-modify-write can't
// interleave even though each step awaits.
const delay = (ms: number) => new Promise((r) => setTimeout(r, ms));

class AtomicCounter {
  private value = 0;
  private queue = Promise.resolve();

  increment(): Promise<number> {
    this.queue = this.queue.then(async () => {
      await delay(10); // async work inside the critical section
      this.value += 1;
      return this.value;
    });

    return this.queue;
  }

  getValue(): number {
    return this.value;
  }
}
