"""Pull user access data from Okta and generate an access review report.

Requires: pip install requests
Usage:
    export OKTA_API_TOKEN=ssws_xxx
    export OKTA_DOMAIN=yourorg.okta.com
    python okta-access-review.py --days 90 --output access_review.csv
"""

import argparse
import csv
import os
from datetime import datetime, timedelta, timezone
from dataclasses import dataclass
from typing import List

import requests


@dataclass
class UserAccessRecord:
    user_id: str
    user_name: str
    status: str
    last_login: str
    assigned_apps: List[str]
    admin_roles: List[str]


class OktaAccessReviewer:
    def __init__(self, api_token: str, domain: str):
        self.headers = {
            "Authorization": f"SSWS {api_token}",
            "Accept": "application/json",
        }
        self.base_url = f"https://{domain}/api/v1"

    def get_inactive_users(self, days: int = 90) -> List[dict]:
        """Find users who haven't logged in within the specified period."""
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)
        users = []
        params = {"filter": 'status eq "ACTIVE"'}
        resp = requests.get(
            f"{self.base_url}/users",
            headers=self.headers,
            params=params,
        )
        resp.raise_for_status()
        for user in resp.json():
            last_login = user.get("lastLogin")
            if not last_login:
                continue
            login_time = datetime.fromisoformat(last_login.replace("Z", "+00:00"))
            if login_time < cutoff:
                users.append({
                    "id": user["id"],
                    "email": user["profile"]["email"],
                    "last_login": last_login,
                    "status": user["status"],
                })
        return users

    def get_user_apps(self, user_id: str) -> List[str]:
        """Get applications assigned to a user."""
        resp = requests.get(
            f"{self.base_url}/users/{user_id}/appLinks",
            headers=self.headers,
        )
        resp.raise_for_status()
        return [app["label"] for app in resp.json()]

    def get_admin_roles(self, user_id: str) -> List[str]:
        """Get admin roles assigned to a user."""
        resp = requests.get(
            f"{self.base_url}/users/{user_id}/roles",
            headers=self.headers,
        )
        resp.raise_for_status()
        return [role["type"] for role in resp.json()]

    def generate_review_report(self, output_file: str) -> None:
        """Generate a CSV report of all active users and their access."""
        resp = requests.get(
            f"{self.base_url}/users",
            headers=self.headers,
            params={"filter": 'status eq "ACTIVE"'},
        )
        resp.raise_for_status()
        with open(output_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "User ID", "Email", "Status", "Last Login",
                "Assigned Apps", "Admin Roles",
            ])
            for user in resp.json():
                apps = self.get_user_apps(user["id"])
                roles = self.get_admin_roles(user["id"])
                writer.writerow([
                    user["id"],
                    user["profile"]["email"],
                    user["status"],
                    user.get("lastLogin", "Never"),
                    "; ".join(apps),
                    "; ".join(roles),
                ])


def main():
    parser = argparse.ArgumentParser(description="Okta access review report")
    parser.add_argument("--days", type=int, default=90, help="Inactivity threshold in days")
    parser.add_argument("--output", default="access_review.csv", help="CSV output file")
    args = parser.parse_args()

    reviewer = OktaAccessReviewer(
        api_token=os.environ["OKTA_API_TOKEN"],
        domain=os.environ["OKTA_DOMAIN"],
    )
    inactive = reviewer.get_inactive_users(days=args.days)
    for u in inactive:
        print(f"INACTIVE: {u['email']} - last login: {u['last_login']}")
    reviewer.generate_review_report(args.output)
    print(f"\nReport written to {args.output}")


if __name__ == "__main__":
    main()
