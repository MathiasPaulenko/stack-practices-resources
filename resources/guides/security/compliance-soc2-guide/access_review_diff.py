#!/usr/bin/env python3
"""Diff two quarterly IAM exports for a SOC 2 access review.

Usage:
    python access_review_diff.py previous.csv current.csv [--out report.md]

Expected CSV columns: user_id,email,role,last_login  (header row required)

Output: a markdown report listing additions, removals, and role changes.
Attach it to the access-review ticket - the ticket plus this diff is the
evidence the auditor samples for CC4/CC6.
"""

import argparse
import csv
import sys
from datetime import date


def load(path: str) -> dict[str, dict[str, str]]:
    with open(path, newline="", encoding="utf-8") as f:
        return {row["user_id"]: row for row in csv.DictReader(f)}


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("previous", help="Last quarter's IAM export (CSV)")
    p.add_argument("current", help="This quarter's IAM export (CSV)")
    p.add_argument("--out", help="Write report to this file instead of stdout")
    args = p.parse_args()

    prev, curr = load(args.previous), load(args.current)
    added = sorted(set(curr) - set(prev))
    removed = sorted(set(prev) - set(curr))
    changed = sorted(
        u for u in set(prev) & set(curr)
        if prev[u]["role"] != curr[u]["role"]
    )
    stale = sorted(
        u for u, r in curr.items()
        if not r.get("last_login") or r["last_login"] < "1900-01-01"
    )

    lines = [
        f"# Access Review Diff - {date.today().isoformat()}",
        "",
        f"- Previous export: `{args.previous}` ({len(prev)} users)",
        f"- Current export: `{args.current}` ({len(curr)} users)",
        "",
        f"## Additions ({len(added)})",
    ]
    lines += [f"- `{u}` - {curr[u]['email']} ({curr[u]['role']})" for u in added] or ["- none"]
    lines += ["", f"## Removals ({len(removed)})"]
    lines += [f"- `{u}` - {prev[u]['email']} (was {prev[u]['role']})" for u in removed] or ["- none"]
    lines += ["", f"## Role changes ({len(changed)})"]
    lines += [
        f"- `{u}` - {prev[u]['role']} -> {curr[u]['role']}" for u in changed
    ] or ["- none"]
    lines += ["", f"## Never logged in ({len(stale)})"]
    lines += [f"- `{u}` - {curr[u]['email']}" for u in stale] or ["- none"]
    lines += [
        "",
        "## Reviewer sign-off",
        "",
        "- [ ] Every addition is expected (new hire or granted request)",
        "- [ ] Every removal is expected (departure or revoked request)",
        "- [ ] Every role change matches an approved ticket",
        "- [ ] Revoked: ____________  Reviewer: ____________  Date: ________",
    ]
    report = "\n".join(lines) + "\n"

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"wrote {args.out}", file=sys.stderr)
    else:
        print(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
