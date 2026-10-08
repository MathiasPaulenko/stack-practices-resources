"""Parallel job control with multiprocessing.Pool.

Each line of jobs.txt is a full shell command. Exit codes come back
in pool.map results — no joblog needed.
"""

import multiprocessing
import shutil
import subprocess
import time
from pathlib import Path

# Resolve bash explicitly — on Windows, CreateProcess would otherwise
# find the WSL launcher in System32 before the real bash on PATH
BASH = shutil.which("bash") or shutil.which("sh") or "bash"


def run_task(task: str) -> tuple[str, int, float]:
    start = time.time()
    result = subprocess.run(
        [BASH, "-c", task],
        capture_output=True,
        text=True,
        timeout=300,
    )
    return task, result.returncode, time.time() - start


def main():
    tasks = Path("jobs.txt").read_text().strip().split("\n")
    max_workers = min(4, multiprocessing.cpu_count())

    with multiprocessing.Pool(max_workers) as pool:
        results = pool.map(run_task, tasks)

    succeeded = sum(1 for _, code, _ in results if code == 0)
    print(f"Total: {len(results)}, Success: {succeeded}, Failed: {len(results) - succeeded}")

    for task, code, elapsed in results:
        status = "OK" if code == 0 else f"FAIL (exit {code})"
        print(f"  {task}: {status} ({elapsed:.1f}s)")


if __name__ == "__main__":
    main()
