#!/usr/bin/env python3
"""Export PR approval trails to CSV for SOC 2 change-management evidence (CC8).

Requires: GITHUB_TOKEN env var (repo scope, read-only is enough).
Usage:
    GITHUB_TOKEN=ghp_... python pr_approval_export.py owner/repo \
        --since 2026-01-01 --out pr_approvals.csv

Writes one row per merged PR: number, title, author, approvers, merged_at.
Archive the CSV monthly — auditors sample it to verify every production
change had an independent approver.
"""

import argparse
import csv
import json
import os
import sys
import urllib.request

API = "https://api.github.com"


def gh(path: str, token: str):
    req = urllib.request.Request(
        f"{API}{path}",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("repo", help="owner/repo")
    p.add_argument("--since", required=True, help="Only PRs merged after this date (YYYY-MM-DD)")
    p.add_argument("--out", default="pr_approvals.csv")
    args = p.parse_args()

    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        sys.exit("GITHUB_TOKEN is not set")

    pulls, page = [], 1
    while True:
        batch = gh(
            f"/repos/{args.repo}/pulls?state=closed&per_page=100&page={page}", token
        )
        if not batch:
            break
        pulls += [pr for pr in batch if pr.get("merged_at") and pr["merged_at"] >= args.since]
        page += 1

    with open(args.out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["pr", "title", "author", "approvers", "merged_at"])
        for pr in pulls:
            reviews = gh(f"/repos/{args.repo}/pulls/{pr['number']}/reviews", token)
            approvers = sorted(
                {r["user"]["login"] for r in reviews if r["state"] == "APPROVED"}
            )
            w.writerow([
                pr["number"], pr["title"], pr["user"]["login"],
                ";".join(approvers), pr["merged_at"],
            ])

    print(f"wrote {len(pulls)} merged PRs to {args.out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
