# Watch File Changes — Companion Examples

Runnable file system watchers in four languages, companion to the
[Watch File Changes recipe](https://stackpractices.com/recipes/watch-file-changes/) on StackPractices.

## Files

| File | Language | What it shows |
| --- | --- | --- |
| `debounced_watcher.py` | Python | watchdog handler that coalesces rapid editor saves into one callback |
| `chokidar-watcher.js` | JavaScript | chokidar with glob filtering, debounce, and `awaitWriteFinish` |
| `RecursiveWatcher.java` | Java | recursive `WatchService` with thread pool, `OVERFLOW` handling, and invalid-key cleanup |
| `watch.sh` | Bash | `inotifywait` watcher with simplified debounce (Linux only) |

## Quick start

```bash
# Python — requires: pip install watchdog
python debounced_watcher.py ./src

# JavaScript — requires: npm install chokidar
node chokidar-watcher.js ./src

# Java — JDK 7+
javac RecursiveWatcher.java && java RecursiveWatcher ./src

# Bash — Linux only, requires: apt install inotify-tools
./watch.sh ./src
```

## Caveats

- `fs.watch` with `{ recursive: true }` needs Node 20+ on Linux — use chokidar for older versions or cross-platform consistency.
- Native watchers can't see changes on network shares (NFS/SMB) or across container bind mounts; use polling there (`usePolling: true` in chokidar, `FileAlterationMonitor` in Java).
- The bash debounce uses a shared cache file — fine for demos, not for concurrent production use.
