// Pattern 4: a FIFO mutex for critical sections in async code.
// acquire() resolves with a release function; waiters queue in order.
class Mutex {
  private locked = false;
  private queue: Array<() => void> = [];

  async acquire(): Promise<() => void> {
    if (!this.locked) {
      this.locked = true;
      return () => this.release();
    }

    return new Promise((resolve) => {
      this.queue.push(() => resolve(() => this.release()));
    });
  }

  private release(): void {
    if (this.queue.length > 0) {
      const next = this.queue.shift()!;
      next();
    } else {
      this.locked = false;
    }
  }
}

// Usage: serialize balance transfers so check-and-act can't interleave.
interface Account {
  balance: number;
}

const balanceMutex = new Mutex();

async function transfer(from: Account, to: Account, amount: number): Promise<void> {
  const release = await balanceMutex.acquire();
  try {
    if (from.balance >= amount) {
      from.balance -= amount;
      to.balance += amount;
    }
  } finally {
    release();
  }
}
