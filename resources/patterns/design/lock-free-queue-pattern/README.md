# Lock-Free Queue Pattern — Runnable Examples

Companion to the [Lock-Free Queue Pattern](https://stackpractices.com/patterns/lock-free-queue-pattern/) on StackPractices.

## Files

| File | What it shows |
|------|---------------|
| `spsc_ring_buffer.py` | Single-producer/single-consumer ring buffer — index ownership, no shared counter |
| `spsc_ring_buffer_batched.py` | Batched variant: publish N items with one `head` update |
| `spsc_ring_buffer.js` | Same SPSC design with `Atomics` + `SharedArrayBuffer` across `worker_threads` |
| `ConcurrentLinkedQueueDemo.java` | MPMC via the JDK's lock-free Michael & Scott queue |
| `mpmc_array_queue.rs` | Bounded MPMC via crossbeam's `ArrayQueue` (Vyukov algorithm) |
| `benchmark_spsc.py` | Throughput comparison: item-by-item vs batched enqueue |

## Run

```bash
python spsc_ring_buffer.py          # Python 3.9+, stdlib only
python spsc_ring_buffer_batched.py
python benchmark_spsc.py            # needs the two files above

node spsc_ring_buffer.js            # Node 18+, ESM

javac ConcurrentLinkedQueueDemo.java && java ConcurrentLinkedQueueDemo

# Rust: create a crate, add `crossbeam = "0.8"`, drop this in src/main.rs
cargo run --release
```

## Notes

- The Python SPSC relies on CPython's GIL for atomic attribute access. For other interpreters or languages, publish `head`/`tail` with release ordering and read the peer index with acquire ordering.
- `mpmc_array_queue.rs` is the recommended approach for real MPMC in Rust — writing a correct bounded MPMC by hand requires per-slot sequence numbers; don't improvise it.
