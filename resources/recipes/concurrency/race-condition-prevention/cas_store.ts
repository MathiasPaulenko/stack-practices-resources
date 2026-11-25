// Pattern 5: optimistic concurrency. compareAndSwap commits only if the
// current value still matches what the caller read; retry on false.
class CASStore<T> {
  private value: T;

  constructor(initial: T) {
    this.value = initial;
  }

  compareAndSwap(expected: T, newValue: T): boolean {
    if (this.value === expected) {
      this.value = newValue;
      return true;
    }
    return false;
  }

  getValue(): T {
    return this.value;
  }
}
