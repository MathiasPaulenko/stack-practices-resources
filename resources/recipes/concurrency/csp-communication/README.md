# CSP Communication — Channels, Select and Fan-out

Runnable examples for the StackPractices recipe
[Coordinate Concurrent Tasks with CSP Channels](https://stackpractices.com/recipes/csp-communication/).

CSP (Communicating Sequential Processes) replaces shared mutable state with
message passing: goroutines/tasks communicate through channels instead of
locks. These examples run the patterns from the recipe end to end.

## Files

| File | What it shows |
|------|---------------|
| `pipeline.go` | Go pipeline (`generator` → `square` → consumer) plus fan-out/fan-in workers coordinated with `sync.WaitGroup` — results channel closed safely after all workers finish. |
| `select_timeout.go` | `select` multiplexing two inputs, nil-channel trick to disable closed cases, `context.Context` cancellation, and a timeout case. |
| `rust_mpsc.rs` | `tokio::sync::mpsc` producer/consumer — bounded channel gives you backpressure for free; `recv()` returns `None` when all senders drop. |
| `ts_pipeline.ts` | TypeScript async generators as channels: a linear pipeline plus a small fan-out over a shared async iterator. |

## Run

```bash
go run pipeline.go
go run select_timeout.go

# Rust (needs tokio = { version = "1", features = ["full"] } in Cargo.toml)
cargo run --bin rust_mpsc

# TypeScript
npx tsx ts_pipeline.ts
```

## Key ideas

- Sender closes the channel; receivers detect it via `range`/`ok`.
- `select` + `ctx.Done()` gives every goroutine a clean exit path — no leaks.
- Buffer channels for bursts, not "just in case": unbuffered channels surface
  coordination bugs early.
- Never count receives blindly; use `sync.WaitGroup` for a fixed worker count.
