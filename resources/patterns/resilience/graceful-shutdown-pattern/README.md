# Graceful Shutdown Pattern — Companion Code

Runnable implementations of the graceful shutdown pattern from the
[StackPractices pattern page](https://stackpractices.com/patterns/graceful-shutdown-pattern/).

## Files

| File | What it shows |
| --- | --- |
| `shutdown/graceful.py` | Python `HTTPServer` that tracks active requests and drains on SIGTERM. |
| `shutdown/graceful.js` | Express server that returns 503 while shutting down and exits when the count hits zero. |
| `shutdown/GracefulShutdownConfig.java` | Spring Boot `Shutdown.GRACEFUL` configuration for the embedded Tomcat. |
| `shutdown/ResourceCleanupHook.java` | `SmartLifecycle` hook that closes DB connections and flushes buffers early in the shutdown sequence. |
| `shutdown/worker.py` | Threaded background worker that finishes in-flight jobs before exiting. |
| `shutdown/deregister.py` | Load balancer deregistration before draining (requires `requests`). |
| `shutdown/phased.py` | Multi-phase shutdown with a timeout per phase. |
| `shutdown/websocket.js` | `ws` WebSocket server that closes clients with code 1001 before exiting. |
| `shutdown/k8s-graceful-shutdown.yaml` | Deployment with `preStop` sleep, readiness probe, and `terminationGracePeriodSeconds`. |

## Quick try

```bash
python shutdown/graceful.py        # then: curl localhost:8080/ and hit Ctrl+C
node shutdown/graceful.js          # needs `npm install express`
node shutdown/websocket.js         # needs `npm install ws`
```

Send SIGTERM mid-request to watch the drain: the server stops accepting new
connections, finishes the ones in flight, and exits cleanly instead of cutting
them off.
