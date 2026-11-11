"""Daily cloud cost anomaly check using AWS Cost Explorer.

Compares yesterday's spend with the trailing 30-day average and flags
days that exceed the threshold (default 120%). Designed to run as a
scheduled job (Lambda/EventBridge, cron pod, CI schedule).

Usage:
    python cost_anomaly_detection.py [--threshold 1.20]

Requires AWS credentials with ce:GetCostAndUsage permission.
"""

from __future__ import annotations

import argparse
import sys
from datetime import date, timedelta

import boto3


def daily_cost(ce, start: date, end: date) -> float:
    """Return total unblended cost for [start, end) in USD."""
    resp = ce.get_cost_and_usage(
        TimePeriod={"Start": str(start), "End": str(end)},
        Granularity="DAILY",
        Metrics=["UnblendedCost"],
    )
    return sum(
        float(day["Total"]["UnblendedCost"]["Amount"])
        for day in resp["ResultsByTime"]
    )


def top_service_movers(ce, day: date, limit: int = 3) -> list[tuple[str, float]]:
    """Return the services with the highest spend on the given day."""
    resp = ce.get_cost_and_usage(
        TimePeriod={"Start": str(day), "End": str(day + timedelta(days=1))},
        Granularity="DAILY",
        Metrics=["UnblendedCost"],
        GroupBy=[{"Type": "DIMENSION", "Key": "SERVICE"}],
    )
    groups = [
        (g["Keys"][0], float(g["Metrics"]["UnblendedCost"]["Amount"]))
        for g in resp["ResultsByTime"][0]["Groups"]
    ]
    return sorted(groups, key=lambda kv: kv[1], reverse=True)[:limit]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--threshold", type=float, default=1.20)
    args = parser.parse_args()

    ce = boto3.client("ce")
    today = date.today()
    yesterday = daily_cost(ce, today - timedelta(days=1), today)
    avg_30d = daily_cost(ce, today - timedelta(days=31), today - timedelta(days=1)) / 30

    if yesterday > avg_30d * args.threshold:
        print(f"ANOMALY: ${yesterday:.2f} vs 30d avg ${avg_30d:.2f}")
        print("Top services yesterday:")
        for svc, cost in top_service_movers(ce, today - timedelta(days=1)):
            print(f"  {svc}: ${cost:.2f}")
        return 1

    print(f"OK: ${yesterday:.2f} vs 30d avg ${avg_30d:.2f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
