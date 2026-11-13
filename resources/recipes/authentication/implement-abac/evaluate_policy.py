#!/usr/bin/env python3
"""Minimal ABAC policy evaluator (stdlib only).

Evaluates a request against a JSON policy file. Each rule matches on
attributes of subject/resource/action/environment; the first matching
rule wins (most-specific-first ordering is the caller's job).

Usage:
  python evaluate_policy.py --demo
  python evaluate_policy.py policy.json request.json
"""
import json
import sys
from datetime import datetime, timezone

DEMO_POLICY = {
    "version": "2026-11-13",
    "default": "deny",
    "rules": [
        {
            "name": "deny-top-secret-outside-office",
            "effect": "deny",
            "when": {"resource.classification": "top-secret",
                     "environment.network_zone": "external"},
        },
        {
            "name": "business-hours-only",
            "effect": "deny",
            "when": {"environment.hour_lt": 6},
        },
        {
            "name": "editors-read-own-department",
            "effect": "allow",
            "when": {"subject.role": "editor",
                     "action": "read",
                     "resource.department": "${subject.department}"},
        },
    ],
}

DEMO_REQUEST = {
    "subject": {"role": "editor", "department": "engineering", "clearance": 2},
    "action": "read",
    "resource": {"type": "document", "department": "engineering",
                 "classification": "internal", "owner": "alice"},
    "environment": {"hour": 14, "network_zone": "office", "device_trusted": True},
}


def resolve(rule_value, request):
    """${path} placeholders read from the request; anything else is literal."""
    if isinstance(rule_value, str) and rule_value.startswith("${"):
        node = request
        for part in rule_value[2:-1].split("."):
            node = node.get(part, {})
        return node if not isinstance(node, dict) else None
    return rule_value


def get(path, request):
    node = request
    for part in path.split("."):
        if not isinstance(node, dict):
            return None
        node = node.get(part)
    return node


def matches(when, request):
    for path, expected in when.items():
        if path.endswith("_lt"):
            actual = get(path[:-3], request)
            if actual is None or not (actual < expected):
                return False
        elif path.endswith("_gt"):
            actual = get(path[:-3], request)
            if actual is None or not (actual > expected):
                return False
        else:
            expected_val = resolve(expected, request)
            actual = get(path, request)
            if isinstance(expected_val, list):
                if actual not in expected_val:
                    return False
            elif actual != expected_val:
                return False
    return True


def evaluate(policy, request):
    env = request.setdefault("environment", {})
    env.setdefault("hour", datetime.now(timezone.utc).hour)
    for rule in policy["rules"]:
        if matches(rule.get("when", {}), request):
            return rule["effect"], rule["name"]
    return policy.get("default", "deny"), "(default)"


def main():
    if len(sys.argv) == 1 or sys.argv[1] == "--demo":
        policy, request = DEMO_POLICY, DEMO_REQUEST
    else:
        policy = json.load(open(sys.argv[1], encoding="utf-8"))
        request = json.load(open(sys.argv[2], encoding="utf-8"))

    effect, rule = evaluate(policy, request)
    print(f"decision: {effect.upper()}  (rule: {rule})")

    for label, req in [
        ("deny-top-secret scenario", {**request, "resource": {
            **request["resource"], "classification": "top-secret"},
            "environment": {**request["environment"], "network_zone": "external"}}),
        ("cross-department scenario", {**request, "resource": {
            **request["resource"], "department": "finance"}}),
        ("after-hours scenario", {**request, "environment": {
            **request["environment"], "hour": 3}}),
    ]:
        e, r = evaluate(policy, req)
        print(f"  {label}: {e.upper()} (rule: {r})")

    return 0 if effect == "allow" else 1


if __name__ == "__main__":
    sys.exit(main())
