"""Weekly vendor posture monitor.

Reads vendor-registry.yaml, runs VendorSecurityCheck on each vendor,
and prints a report. Send it to Slack from CI if a vendor's posture
degrades (see vendor-monitoring.yml).

Requires: requests, pyyaml. Optional: HIBP_API_KEY for breach history.
"""

import argparse
import sys

import yaml

from vendor_security_check import VendorSecurityCheck


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="vendor-registry.yaml")
    args = parser.parse_args()

    with open(args.config, encoding="utf-8") as f:
        vendors = yaml.safe_load(f)["vendors"]

    degraded = False
    for v in vendors:
        check = VendorSecurityCheck(v["name"], v["domain"])
        results = check.run_all()
        print(f"\n{v['name']} ({v['domain']}) — risk: {v.get('risk_level', '?')}")
        for key, value in results.items():
            print(f"  {key}: {value}")
        if results.get("dnssec") == "disabled" and v.get("risk_level") == "high":
            degraded = True

    return 1 if degraded else 0


if __name__ == "__main__":
    sys.exit(main())
