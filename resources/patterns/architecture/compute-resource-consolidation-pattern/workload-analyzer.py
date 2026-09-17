#!/usr/bin/env python3
"""Workload consolidation analyzer.

Reads a JSON file describing workloads (average CPU/memory utilization and
peak hours) and prints which pairs are safe to consolidate onto shared
compute capacity.

Usage:
    python workload-analyzer.py workloads.example.json
    python workload-analyzer.py workloads.example.json --max-cpu 0.8 --max-mem 0.85
"""

import argparse
import itertools
import json
import sys


def can_consolidate(a: dict, b: dict, max_cpu: float, max_mem: float) -> bool:
    """Two workloads can share a resource if their peaks don't overlap and
    their combined average usage stays under the given thresholds."""
    overlapping_peaks = set(a["peak_hours"]) & set(b["peak_hours"])
    combined_cpu = a["cpu_avg"] + b["cpu_avg"]
    combined_mem = a["mem_avg"] + b["mem_avg"]
    return not overlapping_peaks and combined_cpu < max_cpu and combined_mem < max_mem


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workload_file", help="JSON file with a list of workloads")
    parser.add_argument("--max-cpu", type=float, default=0.9,
                        help="max combined average CPU (default: 0.9)")
    parser.add_argument("--max-mem", type=float, default=0.9,
                        help="max combined average memory (default: 0.9)")
    args = parser.parse_args()

    with open(args.workload_file, encoding="utf-8") as f:
        workloads = json.load(f)

    if len(workloads) < 2:
        print("Need at least 2 workloads to evaluate.", file=sys.stderr)
        return 1

    pairs = list(itertools.combinations(workloads, 2))
    safe, unsafe = [], []
    for a, b in pairs:
        (safe if can_consolidate(a, b, args.max_cpu, args.max_mem) else unsafe).append((a, b))

    print(f"Evaluated {len(pairs)} workload pairs "
          f"(thresholds: cpu<{args.max_cpu}, mem<{args.max_mem})\n")

    print("SAFE TO CONSOLIDATE:")
    for a, b in safe:
        print(f"  + {a['name']} + {b['name']} "
              f"(cpu={a['cpu_avg'] + b['cpu_avg']:.2f}, mem={a['mem_avg'] + b['mem_avg']:.2f})")

    print("\nDO NOT CONSOLIDATE:")
    for a, b in unsafe:
        peaks = set(a["peak_hours"]) & set(b["peak_hours"])
        reason = f"overlapping peaks {sorted(peaks)}" if peaks else "combined usage over threshold"
        print(f"  - {a['name']} + {b['name']} ({reason})")

    return 0


if __name__ == "__main__":
    sys.exit(main())
