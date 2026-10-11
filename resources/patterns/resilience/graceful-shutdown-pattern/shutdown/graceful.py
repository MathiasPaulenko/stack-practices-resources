# shutdown/graceful.py — Graceful shutdown for Python HTTP servers
import signal
import threading
import time
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler

class GracefulHTTPServer(HTTPServer):
    """HTTP server with graceful shutdown support."""

    def __init__(self, addr, handler):
        super().__init__(addr, handler)
        self._shutting_down = False
        self._active_requests = 0
        self._lock = threading.Lock()
        self._shutdown_event = threading.Event()

    @property
    def is_shutting_down(self):
        return self._shutting_down

    def request_started(self):
        with self._lock:
            self._active_requests += 1

    def request_finished(self):
        with self._lock:
            self._active_requests -= 1
            if self._shutting_down and self._active_requests == 0:
                self._shutdown_event.set()

    def graceful_shutdown(self, timeout=30):
        """Stop accepting new requests, wait for active ones to finish."""
        print("Starting graceful shutdown...")
        self._shutting_down = True

        # Stop accepting new connections
        self.socket.close()

        # Wait for active requests to complete
        with self._lock:
            if self._active_requests == 0:
                print("No active requests, shutting down immediately")
                return

            print(f"Waiting for {self._active_requests} active requests...")

        if self._shutdown_event.wait(timeout=timeout):
            print("All requests completed, shutting down")
        else:
            print(f"Timeout after {timeout}s, forcing shutdown with "
                  f"{self._active_requests} requests still active")

        # Cleanup resources
        self._cleanup()

    def _cleanup(self):
        """Close database connections, flush buffers, etc."""
        print("Cleaning up resources...")
        # Close database connections
        # Flush log buffers
        # Close file handles
        print("Cleanup complete")


class GracefulRequestHandler(BaseHTTPRequestHandler):
    """Request handler that tracks active requests for graceful shutdown."""

    def handle_one_request(self):
        self.server.request_started()
        try:
            super().handle_one_request()
        finally:
            self.server.request_finished()

    def do_GET(self):
        if self.server.is_shutting_down:
            self.send_response(503)
            self.send_header("Connection", "close")
            self.end_headers()
            self.wfile.write(b'{"error": "Server shutting down"}')
            return

        # Simulate work
        time.sleep(0.5)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'{"status": "ok"}')


# Setup signal handlers
server = GracefulHTTPServer(("0.0.0.0", 8080), GracefulRequestHandler)

def signal_handler(signum, frame):
    server.graceful_shutdown(timeout=30)
    sys.exit(0)

signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

print("Server running on port 8080")
server.serve_forever()
