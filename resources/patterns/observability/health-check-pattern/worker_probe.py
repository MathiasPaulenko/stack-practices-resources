"""Command-based probe for worker processes without an HTTP server.

Usage in Kubernetes:

    livenessProbe:
      exec:
        command: ["python", "/app/worker_probe.py"]

Exit code 0 = healthy, 1 = unhealthy.
"""
import os
import sys

import psycopg2


def check_worker_health() -> bool:
    try:
        conn = psycopg2.connect(os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/demo"))
        cur = conn.cursor()
        # Cheap connectivity probe — if the query runs, the worker is fine
        cur.execute("SELECT 1")
        cur.fetchone()
        cur.close()
        conn.close()
        return True
    except Exception:
        return False


if __name__ == "__main__":
    if check_worker_health():
        print("healthy")
        sys.exit(0)
    print("unhealthy")
    sys.exit(1)
