#!/usr/bin/env python3
"""rightsize_report.py — Flag underutilized instances using p95 CPU.

Reads a CSV of instance metrics (30 days) and prints right-sizing
candidates. Use p95, not average — averages hide bursty workloads
that still need headroom.

Usage:
    python rightsize_report.py instance_metrics.csv [--cpu-threshold 40]

Expected CSV columns:
    instance_id, instance_type, cpu_p95, memory_p95
(cpu_p95/memory_p95 = 95th-percentile utilization over the window, 0-100)
"""

import argparse
import csv
import sys


def load_metrics(path: str) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    required = {"instance_id", "instance_type", "cpu_p95", "memory_p95"}
    if rows and not required.issubset(rows[0].keys()):
        missing = required - set(rows[0].keys())
        sys.exit(f"CSV missing columns: {sorted(missing)}")
    return rows


def find_candidates(rows: list[dict], cpu_threshold: float) -> list[dict]:
    out = []
    for r in rows:
        cpu = float(r["cpu_p95"])
        mem = float(r["memory_p95"])
        if cpu < cpu_threshold:
            out.append({**r, "cpu_p95": cpu, "memory_p95": mem})
    return sorted(out, key=lambda r: r["cpu_p95"])


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("csv", help="instance metrics CSV")
    ap.add_argument("--cpu-threshold", type=float, default=40.0,
                    help="p95 CPU below this = candidate (default 40)")
    ap.add_argument("--terminate-threshold", type=float, default=10.0,
                    help="p95 CPU below this = terminate candidate (default 10)")
    args = ap.parse_args()

    rows = load_metrics(args.csv)
    candidates = find_candidates(rows, args.cpu_threshold)

    if not candidates:
        print("No right-sizing candidates — fleet looks properly sized.")
        return

    print(f"{'Instance':<22}{'Type':<16}{'p95 CPU':>8}{'p95 Mem':>9}  Action")
    print("-" * 66)
    for c in candidates:
        action = "TERMINATE" if c["cpu_p95"] < args.terminate_threshold else "DOWNSIZE"
        print(f"{c['instance_id']:<22}{c['instance_type']:<16}"
              f"{c['cpu_p95']:>7.1f}%{c['memory_p95']:>8.1f}%  {action}")
    print(f"\n{len(candidates)} candidates of {len(rows)} instances.")
    print("Next: verify workload patterns manually, then resize/terminate.")


if __name__ == "__main__":
    main()
