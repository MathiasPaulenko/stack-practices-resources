#!/usr/bin/env python3
"""Audit GitHub org access and flag inactive members."""
import requests
import sys
from datetime import datetime, timedelta

ORG = "your-org"
TOKEN = sys.argv[1] if len(sys.argv) > 1 else ""
HEADERS = {"Authorization": f"token {TOKEN}", "Accept": "application/vnd.github+json"}

def get_org_members() -> list:
    resp = requests.get(f"https://api.github.com/orgs/{ORG}/members", headers=HEADERS)
    return resp.json()

def get_user_activity(username: str) -> dict:
    resp = requests.get(
        f"https://api.github.com/users/{username}/events",
        headers=HEADERS,
        params={"per_page": 1},
    )
    events = resp.json()
    if events:
        last_event = datetime.strptime(events[0]["created_at"], "%Y-%m-%dT%H:%M:%SZ")
        days_inactive = (datetime.utcnow() - last_event).days
        return {"username": username, "last_active": events[0]["created_at"], "days_inactive": days_inactive}
    return {"username": username, "last_active": "never", "days_inactive": 999}

def audit_members() -> None:
    members = get_org_members()
    print(f"Total org members: {len(members)}\n")
    print(f"{'Username':<25} {'Last Active':<25} {'Days Inactive':<15} {'Status'}")
    print("-" * 80)

    threshold = 90
    for member in members:
        username = member["login"]
        activity = get_user_activity(username)
        status = "REVIEW" if activity["days_inactive"] > threshold else "OK"
        print(f"{username:<25} {activity['last_active']:<25} {activity['days_inactive']:<15} {status}")

if __name__ == "__main__":
    audit_members()
