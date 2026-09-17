#!/usr/bin/env python3
"""summarize-week.py — build the executive summary table for a weekly ops review.

Reads a JSON export with the week's incidents and cost rows, prints the
Markdown table for section 1 of the runbook template.

Input JSON shape:

    {
      "incidents": [
        {"severity": "P1", "detect_min": 3, "resolve_min": 25},
        ...
      ],
      "cost_this_week": 12450.0,
      "cost_last_week": 11800.0,
      "cost_budget": 15000.0,
      "error_budget_pct": 78.0,
      "error_budget_last_pct": 82.0
    }

Usage: python summarize-week.py week.json
"""

import json
import sys

SEV_MAP = {"P0": "SEV-1", "P1": "SEV-2"}


def trend(cur: float, prev: float) -> str:
    if prev == 0:
        return "→"
    delta = (cur - prev) / prev
    if delta > 0.05:
        return "↑"
    if delta < -0.05:
        return "↓"
    return "→"


def main(path: str) -> None:
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)

    incidents = data["incidents"]
    sev12 = sum(1 for i in incidents if i["severity"] in SEV_MAP)
    mttr = sum(i["resolve_min"] for i in incidents) / max(len(incidents), 1)

    cost_now = data["cost_this_week"]
    cost_prev = data["cost_last_week"]
    eb_now = data["error_budget_pct"]
    eb_prev = data["error_budget_last_pct"]

    rows = [
        ("Incidents", len(incidents), "-", "→", "< 3"),
        ("SEV 1-2", sev12, "-", "→", "0"),
        ("MTTR (mean)", f"{mttr:.0f} min", "-", "→", "< 30 min"),
        ("Cloud Cost", f"${cost_now:,.0f}", f"${cost_prev:,.0f}", trend(cost_now, cost_prev), f"< ${data['cost_budget']:,.0f}"),
        ("Error Budget Remaining", f"{eb_now:.0f}%", f"{eb_prev:.0f}%", trend(eb_now, eb_prev), "> 50%"),
    ]

    print("| Metric | This Week | Last Week | Trend | Target |")
    print("|--------|-----------|-----------|-------|--------|")
    for name, cur, prev, tr, target in rows:
        print(f"| {name} | {cur} | {prev} | {tr} | {target} |")

    if cost_prev and cost_now / cost_prev > 1.05:
        print(f"\n⚠ Cost up {(cost_now / cost_prev - 1) * 100:.1f}% week-over-week — investigate in section 3.")
    if eb_now < 50:
        print("\n⚠ Error budget below 50% — flag the affected service as at-risk.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass
    main(sys.argv[1])
