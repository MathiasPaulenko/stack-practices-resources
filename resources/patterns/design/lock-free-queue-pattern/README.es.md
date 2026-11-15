# Patrón Lock-Free Queue — Ejemplos Ejecutables

Companion del [Patrón Lock-Free Queue](https://stackpractices.com/es/patterns/lock-free-queue-pattern/) en StackPractices.

## Archivos

| Archivo | Qué muestra |
|---------|-------------|
| `spsc_ring_buffer.py` | Ring buffer single-producer/single-consumer — propiedad de índices, sin contador compartido |
| `spsc_ring_buffer_batched.py` | Variante por lotes: publica N items con una sola actualización de `head` |
| `spsc_ring_buffer.js` | El mismo diseño SPSC con `Atomics` + `SharedArrayBuffer` entre `worker_threads` |
| `ConcurrentLinkedQueueDemo.java` | MPMC con la cola lock-free del JDK (algoritmo Michael & Scott) |
| `mpmc_array_queue.rs` | MPMC acotada con `ArrayQueue` de crossbeam (algoritmo Vyukov) |
| `benchmark_spsc.py` | Comparación de rendimiento: item a item vs encolado por lotes |

## Ejecutar

```bash
python spsc_ring_buffer.py          # Python 3.9+, solo stdlib
python spsc_ring_buffer_batched.py
python benchmark_spsc.py            # necesita los dos archivos anteriores

node spsc_ring_buffer.js            # Node 18+, ESM

javac ConcurrentLinkedQueueDemo.java && java ConcurrentLinkedQueueDemo

# Rust: crea un crate, añade `crossbeam = "0.8"`, pon esto en src/main.rs
cargo run --release
```

## Notas

- El SPSC de Python depende del GIL de CPython para el acceso atómico a atributos. En otros intérpretes o lenguajes, publica `head`/`tail` con orden release y lee el índice del otro hilo con acquire.
- `mpmc_array_queue.rs` es el enfoque recomendado para MPMC real en Rust: escribir una MPMC acotada correcta a mano requiere números de secuencia por slot; no lo improvises.
