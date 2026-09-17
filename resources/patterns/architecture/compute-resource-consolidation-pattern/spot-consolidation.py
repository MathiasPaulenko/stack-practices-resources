#!/usr/bin/env python3
"""Time-window spot instance consolidation.

Groups batch workloads by their allowed execution window and requests one
spot instance per window. Intended as a starting point — pair it with
checkpointing so interrupted jobs can resume.

Usage:
    python spot-consolidation.py workloads-windows.example.json --dry-run
"""

import argparse
import json
import sys


def group_by_window(workloads: list) -> dict:
    windows = {}
    for w in workloads:
        window = (w["start_hour"], w["end_hour"])
        windows.setdefault(window, []).append(w)
    return windows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workload_file", help="JSON file with workloads incl. start_hour/end_hour")
    parser.add_argument("--region", default="us-east-1")
    parser.add_argument("--instance-type", default="m5.large")
    parser.add_argument("--dry-run", action="store_true",
                        help="print the plan without calling the AWS API")
    args = parser.parse_args()

    with open(args.workload_file, encoding="utf-8") as f:
        workloads = json.load(f)

    windows = group_by_window(workloads)
    print(f"{len(workloads)} workloads grouped into {len(windows)} time window(s)\n")

    for window, ws in windows.items():
        total_cpu = sum(w["cpu"] for w in ws)
        total_mem = sum(w["mem"] for w in ws)
        names = ", ".join(w["name"] for w in ws)
        print(f"Window {window[0]:02d}:00-{window[1]:02d}:00 -> {names}")
        print(f"  combined: cpu={total_cpu}m mem={total_mem}Mi -> {args.instance_type}")

        if args.dry_run:
            print("  [dry-run] no spot request sent")
            continue

        import boto3
        ec2 = boto3.client("ec2", region_name=args.region)
        response = ec2.request_spot_instances(
            InstanceCount=1,
            Type="one-time",
            InstanceInterruptionBehavior="terminate",
            LaunchSpecification={
                "ImageId": "ami-12345678",
                "InstanceType": args.instance_type,
            },
        )
        req_id = response["SpotInstanceRequests"][0]["SpotInstanceRequestId"]
        print(f"  requested: {req_id}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
