"""Debounced file watcher with event coalescing (Python, watchdog).

Requires: pip install watchdog
Usage:    python debounced_watcher.py [directory]
"""

import sys
import time
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from typing import Callable


class DebouncedEventHandler(FileSystemEventHandler):
    """Coalesces rapid file events into a single callback after a quiet period."""

    def __init__(self, callback: Callable[[str, str], None],
                 debounce_seconds: float = 0.3,
                 extensions: list[str] | None = None):
        self.callback = callback
        self.debounce = debounce_seconds
        self.extensions = extensions or []
        self._pending: dict[str, dict] = {}
        self._lock = threading.Lock()
        self._timer: threading.Timer | None = None

    def _should_process(self, path: str) -> bool:
        if not self.extensions:
            return True
        return any(path.endswith(ext) for ext in self.extensions)

    def _on_event(self, event_type: str, src_path: str):
        if not self._should_process(src_path):
            return
        with self._lock:
            self._pending[src_path] = {
                "type": event_type,
                "time": time.time(),
            }
            if self._timer:
                self._timer.cancel()
            self._timer = threading.Timer(self.debounce, self._flush)
            self._timer.start()

    def _flush(self):
        with self._lock:
            for path, info in self._pending.items():
                self.callback(info["type"], path)
            self._pending.clear()

    def on_created(self, event):
        if not event.is_directory:
            self._on_event("created", event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            self._on_event("modified", event.src_path)

    def on_deleted(self, event):
        if not event.is_directory:
            self._on_event("deleted", event.src_path)

    def on_moved(self, event):
        if not event.is_directory:
            self._on_event("moved", event.dest_path)


def handle_change(event_type: str, path: str):
    print(f"[{event_type}] {path}")


if __name__ == "__main__":
    watch_dir = sys.argv[1] if len(sys.argv) > 1 else "./src"

    observer = Observer()
    handler = DebouncedEventHandler(
        callback=handle_change,
        debounce_seconds=0.3,
        extensions=[".py", ".js", ".json", ".yaml"],
    )
    observer.schedule(handler, path=watch_dir, recursive=True)
    observer.start()
    print(f"Watching {watch_dir} (Ctrl+C to stop)")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
