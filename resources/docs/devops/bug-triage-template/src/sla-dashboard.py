import os
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import List

SLA_TARGETS = {
    "S1": timedelta(hours=4),
    "S2": timedelta(hours=24),
    "S3": timedelta(days=7),
    "S4": timedelta(days=14),
}

@dataclass
class BugTicket:
    id: str
    severity: str
    created_at: datetime
    status: str
    assignee: str

def find_aged_bugs(tickets: List[BugTicket]) -> List[BugTicket]:
    """Find bugs that have exceeded their SLA resolution target."""
    now = datetime.now()
    aged = []
    for ticket in tickets:
        if ticket.status in ("closed", "resolved"):
            continue
        sla = SLA_TARGETS.get(ticket.severity)
        if not sla:
            continue
        age = now - ticket.created_at
        if age > sla:
            aged.append(ticket)
    return aged

def format_slack_alert(aged_bugs: List[BugTicket]) -> str:
    """Format aged bugs for a Slack alert message."""
    if not aged_bugs:
        return "No bugs have exceeded their SLA target."

    lines = [":warning: *SLA Violation Alert* — Bugs exceeding resolution target:\n"]
    for bug in sorted(aged_bugs, key=lambda b: b.created_at):
        age_hours = (datetime.now() - bug.created_at).total_seconds() / 3600
        sla_hours = SLA_TARGETS[bug.severity].total_seconds() / 3600
        lines.append(
            f"• {bug.severity} {bug.id} — {age_hours:.0f}h old "
            f"(SLA: {sla_hours:.0f}h) — Assigned: {bug.assignee}"
        )
    return "\n".join(lines)

# Example usage
tickets = [
    BugTicket("BUG-100", "S1", datetime.now() - timedelta(hours=6), "open", "alice"),
    BugTicket("BUG-101", "S2", datetime.now() - timedelta(hours=30), "open", "bob"),
    BugTicket("BUG-102", "S3", datetime.now() - timedelta(days=2), "open", "charlie"),
]

aged = find_aged_bugs(tickets)
print(format_slack_alert(aged))
