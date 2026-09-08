// Priority Queue Pattern: generic heap-based priority queue in TypeScript.
// Compile: tsc priority_queue_ts.ts
// Run: node priority_queue_ts.js
class PriorityQueue<T> {
  private heap: { priority: number; data: T }[] = [];

  enqueue(data: T, priority: number): void {
    this.heap.push({ priority, data });
    this.bubbleUp(this.heap.length - 1);
  }

  dequeue(): T | null {
    if (this.heap.length === 0) return null;
    const top = this.heap[0];
    const last = this.heap.pop()!;
    if (this.heap.length > 0) {
      this.heap[0] = last;
      this.bubbleDown(0);
    }
    return top.data;
  }

  peek(): T | null {
    return this.heap.length > 0 ? this.heap[0].data : null;
  }

  size(): number {
    return this.heap.length;
  }

  isEmpty(): boolean {
    return this.heap.length === 0;
  }

  private bubbleUp(idx: number): void {
    while (idx > 0) {
      const parent = Math.floor((idx - 1) / 2);
      if (this.heap[idx].priority <= this.heap[parent].priority) break;
      [this.heap[idx], this.heap[parent]] = [this.heap[parent], this.heap[idx]];
      idx = parent;
    }
  }

  private bubbleDown(idx: number): void {
    while (true) {
      const left = 2 * idx + 1;
      const right = 2 * idx + 2;
      let largest = idx;
      if (left < this.heap.length && this.heap[left].priority > this.heap[largest].priority) largest = left;
      if (right < this.heap.length && this.heap[right].priority > this.heap[largest].priority) largest = right;
      if (largest === idx) break;
      [this.heap[idx], this.heap[largest]] = [this.heap[largest], this.heap[idx]];
      idx = largest;
    }
  }
}

// Usage: support ticket system
interface Ticket { id: string; subject: string; }

const ticketQueue = new PriorityQueue<Ticket>();
ticketQueue.enqueue({ id: "T1", subject: "Question" }, 1);
ticketQueue.enqueue({ id: "T2", subject: "Bug" }, 3);
ticketQueue.enqueue({ id: "T3", subject: "Feature" }, 2);
ticketQueue.enqueue({ id: "T4", subject: "Outage" }, 5);

console.log(ticketQueue.dequeue()?.id); // T4 (Outage)
console.log(ticketQueue.dequeue()?.id); // T2 (Bug)
console.log(ticketQueue.dequeue()?.id); // T3 (Feature)
console.log(ticketQueue.dequeue()?.id); // T1 (Question)

export { PriorityQueue };
