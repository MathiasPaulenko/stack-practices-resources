// SPSC lock-free ring buffer with Atomics + SharedArrayBuffer.
// Run: node spsc_ring_buffer.js
import { Worker, isMainThread, parentPort, workerData } from "worker_threads";

class SpscRingBuffer {
  constructor(capacity) {
    this.capacity = capacity;
    this.buffer = new SharedArrayBuffer(capacity * 4 + 8);
    this.data = new Int32Array(this.buffer, 0, capacity);
    this.indices = new Int32Array(this.buffer, capacity * 4, 2);
    // indices[0] = head (write), indices[1] = tail (read)
  }
}

if (isMainThread) {
  const ring = new SpscRingBuffer(1000);
  for (const role of ["producer", "consumer"]) {
    const w = new Worker(new URL(import.meta.url), {
      workerData: { role, buffer: ring.buffer, capacity: ring.capacity },
    });
    w.on("message", (msg) => console.log(msg));
  }
} else {
  const { role, buffer, capacity } = workerData;
  const data = new Int32Array(buffer, 0, capacity);
  const indices = new Int32Array(buffer, capacity * 4, 2);

  if (role === "producer") {
    for (let i = 0; i < 10000; i++) {
      let head = Atomics.load(indices, 0);
      while (head - Atomics.load(indices, 1) >= capacity) {}
      Atomics.store(data, head % capacity, i);
      Atomics.store(indices, 0, head + 1);
    }
    parentPort.postMessage("Producer done: 10000 items");
  } else {
    for (let i = 0; i < 10000; i++) {
      let tail = Atomics.load(indices, 1);
      while (tail >= Atomics.load(indices, 0)) {}
      Atomics.load(data, tail % capacity);
      Atomics.store(indices, 1, tail + 1);
    }
    parentPort.postMessage("Consumer done: 10000 items");
  }
}
