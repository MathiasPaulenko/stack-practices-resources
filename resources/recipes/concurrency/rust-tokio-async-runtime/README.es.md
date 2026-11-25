# Runtime Async de Rust con Tokio

Proyecto Cargo ejecutable con los ejemplos de Tokio de la receta de StackPractices: <https://stackpractices.com/es/recipes/rust-tokio-async-runtime/>

## Archivos

- `Cargo.toml` — tokio con `full` activado.
- `src/bin/basic_spawn.rs` — spawn de dos tasks y await de sus resultados.
- `src/bin/channels.rs` — channels `mpsc`, `oneshot` y `broadcast`.
- `src/bin/shared_state.rs` — contador `Arc<Mutex<T>>` actualizado por 10 tasks.
- `src/bin/graceful_shutdown.rs` — workers que se detienen con un `CancellationToken`.
- `src/bin/semaphore.rs` — concurrencia acotada con `Semaphore` (máx. 3 a la vez).

## Uso

```bash
cargo run --bin basic_spawn
cargo run --bin channels
cargo run --bin shared_state
cargo run --bin graceful_shutdown
cargo run --bin semaphore
```

Cada binario es autocontenido; elige la primitiva que estés evaluando.
