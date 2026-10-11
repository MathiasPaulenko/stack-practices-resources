# shutdown/phased.py — Multi-phase shutdown with ordered cleanup
class PhasedShutdown:
    """Shuts down in phases: stop accepting, drain, cleanup, exit.
    Each phase has its own timeout."""

    def __init__(self):
        self._phases = [
            ("stop_accepting", self._stop_accepting, 5),
            ("drain_requests", self._drain_requests, 20),
            ("close_connections", self._close_connections, 5),
            ("flush_buffers", self._flush_buffers, 3),
            ("cleanup", self._cleanup, 2),
        ]

    def _stop_accepting(self):
        print("Phase 1: Stop accepting new requests")

    def _drain_requests(self):
        print("Phase 2: Drain active requests")

    def _close_connections(self):
        print("Phase 3: Close database and MQ connections")

    def _flush_buffers(self):
        print("Phase 4: Flush log and metric buffers")

    def _cleanup(self):
        print("Phase 5: Final cleanup")

    def execute(self):
        for name, handler, timeout in self._phases:
            print(f"Starting phase: {name} (timeout: {timeout}s)")
            handler()
        print("All phases complete, exiting")
