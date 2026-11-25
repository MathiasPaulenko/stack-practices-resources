# Rust Tokio Async Runtime

Runnable Cargo project with the Tokio examples from the StackPractices recipe: <https://stackpractices.com/recipes/rust-tokio-async-runtime/>

## Files

- `Cargo.toml` — tokio with `full` features.
- `src/bin/basic_spawn.rs` — spawn two tasks and await their results.
- `src/bin/channels.rs` — `mpsc`, `oneshot`, and `broadcast` channels.
- `src/bin/shared_state.rs` — `Arc<Mutex<T>>` counter updated by 10 tasks.
- `src/bin/graceful_shutdown.rs` — workers that stop on a `CancellationToken`.
- `src/bin/semaphore.rs` — bounded concurrency with `Semaphore` (max 3 at once).

## Usage

```bash
cargo run --bin basic_spawn
cargo run --bin channels
cargo run --bin shared_state
cargo run --bin graceful_shutdown
cargo run --bin semaphore
```

Each binary is self-contained; pick whichever primitive you're evaluating.
