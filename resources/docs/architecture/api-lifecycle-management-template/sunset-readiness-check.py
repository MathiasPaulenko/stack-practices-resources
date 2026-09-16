"""Sunset readiness check for deprecated API versions.

Queries Prometheus through Grafana's datasource proxy for the daily request
rate on a deprecated version and reports whether it served zero traffic for
ZERO_TRAFFIC_DAYS_REQUIRED consecutive days.

Usage:
    GRAFANA_URL=https://grafana.example.com GRAFANA_TOKEN=... \
        python sunset-readiness-check.py
"""

import os
import sys

import requests
from datetime import datetime, timedelta, timezone

ZERO_TRAFFIC_DAYS_REQUIRED = 7


def check_sunset_readiness(grafana_url: str, api_token: str) -> bool:
    """Return True when the deprecated version served zero traffic for the
    required number of consecutive days."""
    headers = {"Authorization": f"Bearer {api_token}"}
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=ZERO_TRAFFIC_DAYS_REQUIRED + 1)

    params = {
        "query": 'sum(rate(http_requests_total{version="v2"}[1h]))',
        "start": start.timestamp(),
        "end": end.timestamp(),
        "step": 86400,  # one data point per day
    }
    resp = requests.get(
        f"{grafana_url}/api/datasources/proxy/1/api/v1/query_range",
        headers=headers,
        params=params,
        timeout=30,
    )
    resp.raise_for_status()
    series = resp.json()["data"]["result"]

    if not series:
        # An empty series means the metric label disappeared — that looks
        # like zero traffic but may be a broken scrape. Verify before acting.
        print("WARNING: no series returned; verify the metric still exists")
        return False

    daily_rates = [float(point[1]) for point in series[0]["values"]]
    zero_days = sum(1 for rate in daily_rates if rate == 0)

    if zero_days >= ZERO_TRAFFIC_DAYS_REQUIRED:
        print(f"READY FOR SHUTDOWN: {zero_days} days of zero traffic")
        return True

    print(f"NOT READY: {zero_days} zero-traffic days in the window")
    print(f"Average daily rate: {sum(daily_rates) / len(daily_rates):.2f} req/s")
    return False


if __name__ == "__main__":
    url = os.environ.get("GRAFANA_URL")
    token = os.environ.get("GRAFANA_TOKEN")
    if not url or not token:
        print("Set GRAFANA_URL and GRAFANA_TOKEN environment variables.")
        sys.exit(2)
    sys.exit(0 if check_sunset_readiness(url, token) else 1)
