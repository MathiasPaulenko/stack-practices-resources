"""LLM cost monitor — reference implementation.

Feed it a budget config (budget_config.yaml) and a JSONL file of per-request
log entries (one JSON object per line, matching the schema in section 2 of the
StackPractices template) and it prints the alerts to fire plus a daily report.

Usage:
    pip install pyyaml
    python llm_cost_monitor.py --config budget_config.yaml --log usage.jsonl [--date 2026-07-04]

Run it on a schedule — hourly is the right cadence for most workloads.
"""

import argparse
import datetime
import json
import sys
from collections import defaultdict


class LLMCostMonitor:
    def __init__(self, budget_config: dict):
        self.config = budget_config
        self.daily_spend = defaultdict(float)
        self.feature_spend = defaultdict(lambda: defaultdict(float))

    def record(self, request: dict):
        date = request["timestamp"][:10]
        cost = request["total_cost"]
        feature = request["feature"]

        self.daily_spend[date] += cost
        self.feature_spend[date][feature] += cost

    def check_budget(self, date: str) -> dict:
        monthly_spend = sum(
            spend for d, spend in self.daily_spend.items()
            if d.startswith(date[:7])
        )
        budget = self.config["monthly_budget"]
        utilization = monthly_spend / budget

        alerts = []
        for threshold in self.config["alert_thresholds"]:
            if utilization >= threshold["percentage"] / 100:
                alerts.append({
                    "threshold": threshold["percentage"],
                    "action": threshold["action"],
                    "spend": monthly_spend,
                    "budget": budget,
                })

        return {
            "monthly_spend": monthly_spend,
            "budget": budget,
            "utilization": utilization,
            "alerts": alerts,
        }

    def daily_report(self, date: str) -> dict:
        return {
            "date": date,
            "total_spend": self.daily_spend[date],
            "by_feature": dict(self.feature_spend[date]),
        }


def main() -> int:
    parser = argparse.ArgumentParser(description="LLM cost monitor")
    parser.add_argument("--config", required=True, help="Path to budget_config.yaml")
    parser.add_argument("--log", required=True, help="JSONL file with one usage record per line")
    parser.add_argument("--date", default=None, help="Report date (YYYY-MM-DD); defaults to the latest in the log")
    args = parser.parse_args()

    try:
        import yaml
    except ImportError:
        print("pyyaml is required: pip install pyyaml", file=sys.stderr)
        return 2

    with open(args.config, encoding="utf-8") as f:
        config = yaml.safe_load(f)

    monitor = LLMCostMonitor(config)

    with open(args.log, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                monitor.record(json.loads(line))

    date = args.date or max(monitor.daily_spend, default=datetime.date.today().isoformat())

    result = {
        "budget_check": monitor.check_budget(date),
        "daily_report": monitor.daily_report(date),
    }
    print(json.dumps(result, indent=2, default=str))

    return 1 if any(a["action"] == "throttle" for a in result["budget_check"]["alerts"]) else 0


if __name__ == "__main__":
    sys.exit(main())
