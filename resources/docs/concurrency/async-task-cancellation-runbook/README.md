# Async Task Cancellation Runbook — Companion Resources

Companion files for the [Async Task Cancellation Runbook](https://stackpractices.com/docs/async-task-cancellation-runbook/) on StackPractices.com.

## What's included

| File | Language | Description |
|------|----------|-------------|
| `python_cancel.py` | Python | Cooperative cancellation with `asyncio.CancelledError`, `wait_for` timeout, and a `GracefulShutdown` class for SIGINT/SIGTERM |
| `node_cancel.mjs` | JavaScript | `AbortController`/`AbortSignal` cancellation, signal-aware `sleep`, fetch timeout helper |
| `go_cancel.go` | Go | `context.Context` cancellation with `WithTimeout` and `ctx.Done()` checkpoints |
| `JavaCancel.java` | Java | `Future.cancel(true)` interrupt-based cancellation and cleanup |

## Quick start

Each file is self-contained and auto-cancels the demo task after ~2 seconds so you can watch the cleanup path run.

```bash
python python_cancel.py        # Ctrl+C also triggers the signal path
node node_cancel.mjs           # requires Node 18+ (top-level await, DOMException)
go run go_cancel.go
javac JavaCancel.java && java JavaCancel
```

## What to look for

- The task prints `processing item N` until the cancel fires, then runs `cleanup_resources` and re-raises/rethrows the cancellation.
- In `node_cancel.mjs`, `cleanupResources` calls `sleep(50)` *without* a signal — the optional-signal pattern is what makes post-abort cleanup safe.
- In `go_cancel.go`, `defer cancel()` is required; skipping it leaks the context's timer goroutine.
- In `JavaCancel.java`, try `future.cancel(false)` and notice the task keeps running in the background.
