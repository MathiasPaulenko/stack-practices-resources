#!/usr/bin/env python3
"""Estimate monthly AWS Lambda costs for one or more workloads.

Usage:
    python estimate-costs.py workloads.json
    python estimate-costs.py --invocations 10000000 --duration-ms 200 --memory-mb 512

Input JSON format (list of workloads):
    [
      {"name": "processOrder", "invocations": 10000000, "duration_ms": 200,
       "memory_mb": 512, "pc_gb_seconds": 0, "data_out_gb": 5}
    ]

Prices are us-east-1 defaults; override with the PRICE_* constants below
or verify at https://aws.amazon.com/lambda/pricing/ before presenting estimates.
"""

import argparse
import json
import sys

# us-east-1 pricing (verify before use)
PRICE_GB_SECOND_X86 = 0.0000166667
PRICE_GB_SECOND_ARM64 = 0.0000133334
PRICE_PC_GB_SECOND_X86 = 0.0000097222
PRICE_PC_GB_SECOND_ARM64 = 0.0000077778
PRICE_PC_CAPACITY_GB_SECOND_X86 = 0.0000041667
PRICE_PC_CAPACITY_GB_SECOND_ARM64 = 0.0000033334
PRICE_PER_MILLION_REQUESTS = 0.20
PRICE_DATA_OUT_GB = 0.09
FREE_TIER_GB_SECONDS = 400_000
FREE_TIER_REQUESTS = 1_000_000
FREE_TIER_DATA_GB = 100


def estimate_lambda_cost(
    invocations: int,
    avg_duration_ms: float,
    memory_mb: int,
    provisioned_concurrency_gb_seconds: int = 0,
    data_transfer_out_gb: float = 0,
    arch: str = "x86",
) -> dict:
    """Estimate monthly AWS Lambda cost for a single function."""
    duration_s = avg_duration_ms / 1000
    memory_gb = memory_mb / 1024
    gb_seconds = invocations * duration_s * memory_gb

    # With provisioned concurrency the free tier doesn't apply and
    # execution duration bills at the lower PC rate.
    has_pc = provisioned_concurrency_gb_seconds > 0
    if has_pc:
        duration_rate = (
            PRICE_PC_GB_SECOND_ARM64 if arch == "arm64" else PRICE_PC_GB_SECOND_X86
        )
        free_gb_seconds = 0
        free_requests = 0
    else:
        duration_rate = (
            PRICE_GB_SECOND_ARM64 if arch == "arm64" else PRICE_GB_SECOND_X86
        )
        free_gb_seconds = FREE_TIER_GB_SECONDS
        free_requests = FREE_TIER_REQUESTS

    compute_cost = max(gb_seconds - free_gb_seconds, 0) * duration_rate
    request_cost = (max(invocations - free_requests, 0) / 1_000_000) * PRICE_PER_MILLION_REQUESTS

    pc_capacity_rate = (
        PRICE_PC_CAPACITY_GB_SECOND_ARM64 if arch == "arm64" else PRICE_PC_CAPACITY_GB_SECOND_X86
    )
    pc_cost = provisioned_concurrency_gb_seconds * pc_capacity_rate

    billable_data = max(data_transfer_out_gb - FREE_TIER_DATA_GB, 0)
    data_cost = billable_data * PRICE_DATA_OUT_GB

    total = compute_cost + request_cost + pc_cost + data_cost

    return {
        "compute_cost": round(compute_cost, 2),
        "request_cost": round(request_cost, 2),
        "provisioned_concurrency_cost": round(pc_cost, 2),
        "data_transfer_cost": round(data_cost, 2),
        "total_monthly_cost": round(total, 2),
        "gb_seconds": int(gb_seconds),
    }


def print_estimate(name: str, cost: dict) -> None:
    print(f"{name}")
    print(f"  Compute:      ${cost['compute_cost']:>10,.2f}")
    print(f"  Requests:     ${cost['request_cost']:>10,.2f}")
    print(f"  Prov. conc.:  ${cost['provisioned_concurrency_cost']:>10,.2f}")
    print(f"  Data out:     ${cost['data_transfer_cost']:>10,.2f}")
    print(f"  Total:        ${cost['total_monthly_cost']:>10,.2f}/month")
    print(f"  GB-seconds:   {cost['gb_seconds']:>10,}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("json_file", nargs="?", help="JSON file with workload list")
    parser.add_argument("--invocations", type=int, help="Monthly invocations")
    parser.add_argument("--duration-ms", type=float, help="Average duration in ms")
    parser.add_argument("--memory-mb", type=int, help="Allocated memory in MB")
    parser.add_argument("--pc-gb-seconds", type=int, default=0,
                        help="Provisioned concurrency GB-seconds/month")
    parser.add_argument("--data-out-gb", type=float, default=0,
                        help="Data transfer out in GB/month")
    parser.add_argument("--arch", choices=["x86", "arm64"], default="x86")
    args = parser.parse_args()

    if args.json_file:
        with open(args.json_file, encoding="utf-8") as f:
            workloads = json.load(f)
    elif args.invocations and args.duration_ms and args.memory_mb:
        workloads = [{
            "name": "function",
            "invocations": args.invocations,
            "duration_ms": args.duration_ms,
            "memory_mb": args.memory_mb,
            "pc_gb_seconds": args.pc_gb_seconds,
            "data_out_gb": args.data_out_gb,
        }]
    else:
        parser.error("provide a JSON file or --invocations/--duration-ms/--memory-mb")

    grand_total = 0.0
    for w in workloads:
        cost = estimate_lambda_cost(
            invocations=w["invocations"],
            avg_duration_ms=w["duration_ms"],
            memory_mb=w["memory_mb"],
            provisioned_concurrency_gb_seconds=w.get("pc_gb_seconds", 0),
            data_transfer_out_gb=w.get("data_out_gb", 0),
            arch=args.arch,
        )
        print_estimate(w.get("name", "function"), cost)
        grand_total += cost["total_monthly_cost"]

    if len(workloads) > 1:
        print(f"\nGrand total: ${grand_total:,.2f}/month")

    return 0


if __name__ == "__main__":
    sys.exit(main())
