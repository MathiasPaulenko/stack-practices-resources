# Concurrent Patterns with Go Goroutines and Channels — Companion Code

Runnable companion code for the StackPractices recipe
[Concurrent Patterns with Go Goroutines and Channels](https://stackpractices.com/recipes/go-goroutines-channels-patterns/).

Every file is a standalone `package main` program you can run directly:

```bash
go run 01-basic-goroutines.go
```

## Files

| File | Pattern |
| --- | --- |
| `01-basic-goroutines.go` | Goroutines + channels with `sync.WaitGroup` and channel close |
| `02-worker-pool.go` | Worker pool: N workers reading jobs, writing results |
| `03-fan-out-fan-in.go` | Fan-out to 4 workers, fan-in merge into one channel |
| `04-pipeline.go` | Multi-stage pipeline: generate → filter → transform → collect |
| `05-context-timeout.go` | `context.WithTimeout` cancellation in a worker loop |
| `06-rate-limiting.go` | Rate limiting with `time.NewTicker` |
| `07-select-channels.go` | `select` multiplexing tick/boom/default |
| `08-errgroup.go` | Error-aware fan-out with `golang.org/x/sync/errgroup` |
| `09-bounded-semaphore.go` | Bounded parallelism with a semaphore channel |
| `10-done-channel.go` | Cancellation with a dedicated `done` channel |
| `11-tee-channel.go` | Generic `tee` that splits one channel into two |

## Requirements

- Go 1.21 or later.
- `08-errgroup.go` needs `golang.org/x/sync/errgroup`; run `go mod tidy` once to fetch it.

## Notes

- `10-done-channel.go` is the idiomatic "stop signal" pattern; in real code prefer `context.Context` as shown in `05-context-timeout.go`.
- `07-select-channels.go` uses `time.NewTicker` + `defer ticker.Stop()` — avoid `time.Tick` in long-running programs because its ticker can never be stopped.
